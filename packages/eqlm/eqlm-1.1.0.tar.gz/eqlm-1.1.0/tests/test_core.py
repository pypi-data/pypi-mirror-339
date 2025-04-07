from itertools import product
from unittest import TestCase
from eqlm import core, img as eqimg
from eqlm.img import color_transforms
from eqlm.utils import filerelpath


class ProcessTest(TestCase):
    def test_biprocess(self):
        for mode, vertical, horizontal, interpolation, target, median, clamp in product(core.Mode, [2, 4], [2, 3], core.Interpolation, [0.0, 0.5, 1.0], [True, False], [True, False]):
            with self.subTest(mode=mode, vertical=vertical, horizontal=horizontal, interpolation=interpolation, target=target, median=median, clamp=clamp):
                x, _ = eqimg.load_image(filerelpath("tsurumai.webp"), normalize=True, orientation=True)
                f, g = color_transforms(mode.value.color, transpose=True)
                v = f(x)
                c = mode.value.channel
                v[c] = core.biprocess(v[c], n=(vertical, horizontal), interpolation=(interpolation, interpolation), target=target, median=median, clamp=clamp, clip=(mode.value.min, mode.value.max))
                y = g(v)
                self.assertEqual(x.shape, y.shape)
