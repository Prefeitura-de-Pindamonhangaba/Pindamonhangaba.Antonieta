import ast
from pathlib import Path
import unittest


class RuntimeCompatibilityTests(unittest.TestCase):
    def test_annotations_support_the_production_python39_runtime(self):
        root = Path(__file__).resolve().parents[1]
        paths = [root / 'main.py', root / 'cors_config.py']
        for directory in ('controllers', 'services', 'dtos', 'models'):
            paths.extend((root / directory).glob('*.py'))
        for path in paths:
            tree = ast.parse(path.read_text(encoding='utf-8'))
            annotations = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.arg, ast.AnnAssign)) and node.annotation:
                    annotations.append(node.annotation)
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.returns:
                    annotations.append(node.returns)
            for annotation in annotations:
                with self.subTest(path=str(path.relative_to(root)), line=annotation.lineno):
                    self.assertFalse(any(isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)
                                         for node in ast.walk(annotation)),
                                     'Use typing.Optional/Union for the Python 3.9 production runtime')
