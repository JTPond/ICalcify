import json
import tempfile
import unittest
from pathlib import Path

import msgpack as msg
import msgpack_numpy as m
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

matplotlib.use("Agg")

import ICalcify as ic
import ICalcify.fitting as ft
from ICalcify.branches import (
    BinBranch,
    Branch,
    FloatBranch,
    FourMatBranch,
    FourVecBranch,
    ObjectBranch,
    PointBinBranch,
    PointBranch,
    StringBranch,
    ThreeMatBranch,
    ThreeVecBranch,
)

m.patch()


class TestBranches(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_object_branch(self):
        b = Branch("obj", "Object", [{"a": 1}, {"a": 2}])
        self.assertIsInstance(b, ObjectBranch)
        self.assertEqual(len(b), 2)
        self.assertIn("Name: 'obj'", repr(b))
        self.assertIn("Type: 'Object'", str(b))
        self.assertIn("<h3>", b._repr_html_())
        self.assertEqual(list(b), [{"a": 1}, {"a": 2}])

        cut_b = b.cut(lambda x: x["a"] > 1)
        self.assertEqual(cut_b.name, "obj_Cut")
        self.assertEqual(len(cut_b), 1)
        self.assertEqual(list(cut_b), [{"a": 2}])

        with self.assertRaises(TypeError):
            ObjectBranch("bad", "Object", 123)

    def test_string_and_float_branches(self):
        sb = Branch("s", "String", ["hello", "world"])
        self.assertIsInstance(sb, StringBranch)
        self.assertEqual(len(sb), 2)

        fb1 = Branch("f1", "f64", [1.0, 2.0, 3.0])
        fb2 = Branch("f2", "f64", [2.0, 4.0, 6.0])
        self.assertIsInstance(fb1, FloatBranch)

        pb = fb1.against(fb2)
        self.assertIsInstance(pb, PointBranch)
        self.assertEqual(pb.name, "f1 X f2")
        np.testing.assert_allclose(pb.branch, np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0]]))

        with self.assertRaises(TypeError):
            fb1.against(sb)
        with self.assertRaises(RuntimeError):
            fb1.against(Branch("f3", "f64", [1.0]))

        fb1.plot(show=False, flag="test")

    def test_vector_and_matrix_branches(self):
        tv = Branch("tv", "ThreeVec", [{"x0": 1.0, "x1": 2.0, "x2": 3.0}])
        self.assertIsInstance(tv, ThreeVecBranch)
        np.testing.assert_allclose(tv.branch, np.array([[1.0, 2.0, 3.0]]))
        tv.scatter(show=False)

        tm = Branch(
            "tm",
            "ThreeMat",
            [{"r0": {"x0": 1.0, "x1": 0.0, "x2": 0.0}, "r1": {"x0": 0.0, "x1": 1.0, "x2": 0.0}, "r2": {"x0": 0.0, "x1": 0.0, "x2": 1.0}}],
        )
        self.assertIsInstance(tm, ThreeMatBranch)
        self.assertEqual(tm.branch.shape, (1, 3, 3))

        fv = Branch("fv", "FourVec", [{"x0": 1.0, "x1": 2.0, "x2": 3.0, "x3": 4.0}])
        self.assertIsInstance(fv, FourVecBranch)
        np.testing.assert_allclose(fv.branch, np.array([[1.0, 2.0, 3.0, 4.0]]))

        fm = Branch(
            "fm",
            "FourMat",
            [
                {
                    "r0": {"x0": 1.0, "x1": 0.0, "x2": 0.0, "x3": 0.0},
                    "r1": {"x0": 0.0, "x1": 1.0, "x2": 0.0, "x3": 0.0},
                    "r2": {"x0": 0.0, "x1": 0.0, "x2": 1.0, "x3": 0.0},
                    "r3": {"x0": 0.0, "x1": 0.0, "x2": 0.0, "x3": 1.0},
                }
            ],
        )
        self.assertIsInstance(fm, FourMatBranch)
        self.assertEqual(fm.branch.shape, (1, 4, 4))

    def test_bin_and_point_bin_branches(self):
        bb_dict = Branch("bins", "Bin", [{"count": 5, "range": [0.0, 1.0]}, {"count": 10, "range": [1.0, 2.0]}])
        self.assertIsInstance(bb_dict, BinBranch)
        self.assertEqual(len(bb_dict), 2)
        self.assertIn("range(0.0, 1.0)", str(bb_dict))
        bb_dict.plot(show=False)

        bb_long = Branch("Time", "Bin", [[i, [i, i + 1]] for i in range(30)])
        self.assertIn("...", str(bb_long))
        cut_bb = bb_long.cut(lambda x: x[1][0] >= 10)
        self.assertEqual(len(cut_bb), 20)

        pbb = Branch(
            "pbin",
            "PointBin",
            [
                {"count": 1, "range": [0.0, 1.0, 0.0, 1.0]},
                {"count": 2, "range": [0.0, 1.0, 1.0, 2.0]},
                {"count": 3, "range": [1.0, 2.0, 0.0, 1.0]},
                {"count": 4, "range": [1.0, 2.0, 1.0, 2.0]},
            ],
        )
        self.assertIsInstance(pbb, PointBinBranch)
        self.assertEqual(len(pbb), 4)
        pbb.plot(show=False)

        with self.assertRaises(ValueError):
            Branch("invalid", "UnknownType", [])


class TestFitting(unittest.TestCase):
    def tearDown(self):
        plt.close("all")

    def test_fitting_functions_and_point_fit(self):
        xs = np.linspace(0.0, 5.0, 25)
        ys = ft.linear(xs, 2.5, 1.0)
        pb = Branch("lin", "Point", [{"x": float(x), "y": float(y)} for x, y in zip(xs, ys)])
        pb.plot(show=False)
        pb.scatter(show=False)

        res = pb.fit(ft.linear)
        np.testing.assert_allclose(res.popt, [2.5, 1.0], rtol=1e-5)
        self.assertIn("Parameters:", repr(res))
        self.assertIn("<h3>Parameters:</h3>", res._repr_html_())
        res.plot(show=False, error=True)

        self.assertAlmostEqual(ft.Gaussian(0.0, 1.0, 0.0, 1.0), 1.0)
        self.assertGreater(ft.BreitWigner(1.0, 1.0, 1.0, 0.5), 0.0)
        self.assertAlmostEqual(ft.exponential(0.0, 2.0, 1.0, 3.0), 5.0)
        self.assertAlmostEqual(ft.poly2(2.0, 1.0, 2.0, 3.0), 17.0)
        self.assertAlmostEqual(ft.poly3(2.0, 1.0, 1.0, 1.0, 1.0), 15.0)
        self.assertAlmostEqual(ft.poly4(2.0, 1.0, 1.0, 1.0, 1.0, 1.0), 31.0)


class TestTreeAndExplorer(unittest.TestCase):
    def setUp(self):
        self.sample_tree_dict = {
            "Name": "test_tree",
            "Desc": "Unit test tree",
            "branches": {
                "vals": {"subtype": "f64", "branch": [1.0, 2.0, 3.0]},
                "pts": {"subtype": "Point", "branch": [{"x": 0.0, "y": 1.0}, {"x": 1.0, "y": 2.0}]},
            },
        }
        self.sample_feed_dict = {
            "Name": "feed_tree",
            "SubType": "String",
            "datafeeds": {
                " greetings": ["hi", "there"],
            },
        }

    def test_tree_from_dict_and_methods(self):
        original = dict(self.sample_tree_dict)
        t = ic.Tree.from_dict(self.sample_tree_dict)
        # Ensure caller dict was not mutated
        self.assertIn("branches", self.sample_tree_dict)
        self.assertEqual(self.sample_tree_dict, original)

        self.assertEqual(len(t), 2)
        self.assertIn("vals", t)
        self.assertIn("Name", t)
        self.assertNotIn("missing", t)
        self.assertEqual(t["Name"], "test_tree")
        self.assertIsInstance(t["vals"], FloatBranch)
        self.assertIn("vals", t._ipython_key_completions_())
        self.assertIn("test_tree", repr(t))
        self.assertIn("test_tree", str(t))
        self.assertIn("test_tree", t._repr_html_())
        self.assertEqual(list(t), ["vals", "pts"])

        with self.assertRaises(KeyError):
            _ = t["missing"]

        ft_tree = ic.Tree.from_dict(self.sample_feed_dict)
        self.assertEqual(len(ft_tree), 1)

        with self.assertRaises(RuntimeError):
            ic.Tree.from_dict({"Name": "bad"})

    def test_empty_tree_formatting(self):
        empty = ic.Tree()
        self.assertIn("EMPTY", repr(empty))
        self.assertIn("EMPTY", str(empty))
        self.assertIn("EMPTY", empty._repr_html_())

    def test_read_and_explorer(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            json_file = tmppath / "sample.json"
            msg_file = tmppath / "sample_msg.msg"

            json_file.write_text(json.dumps(self.sample_tree_dict), encoding="utf-8")
            msg_file.write_bytes(msg.packb(self.sample_tree_dict, default=m.encode))

            # Direct read
            t_json = ic.read(json_file)
            self.assertEqual(t_json["Name"], "test_tree")
            t_msg = ic.read(msg_file)
            self.assertEqual(t_msg["Name"], "test_tree")

            # Buffered Explorer
            exp = ic.New([str(json_file), str(msg_file)], buffer=True)
            self.assertEqual(len(exp), 2)
            self.assertIn("sample", exp)
            self.assertIn("*buffered", repr(exp))
            self.assertIn("&#8250;", exp._repr_html_())

            # Accessing triggers load
            loaded_tree = exp["sample"]
            self.assertEqual(loaded_tree["Name"], "test_tree")
            exp.load_all()
            self.assertNotIn("*buffered", repr(exp))
            self.assertIn("&#8964;", exp._repr_html_())

            exp["custom"] = ic.Tree()
            self.assertIn("custom", exp._ipython_key_completions_())
            with self.assertRaises(KeyError):
                _ = exp["unknown"]


if __name__ == "__main__":
    unittest.main()
