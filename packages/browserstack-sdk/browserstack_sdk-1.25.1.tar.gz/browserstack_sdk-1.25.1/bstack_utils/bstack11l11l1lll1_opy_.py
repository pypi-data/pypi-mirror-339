# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l11111l_opy_
from browserstack_sdk.bstack1ll11l1l1l_opy_ import bstack1111l111_opy_
def _11l11ll11ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11ll1l1l_opy_:
    def __init__(self, handler):
        self._11l11ll1ll1_opy_ = {}
        self._11l11llll11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1111l111_opy_.version()
        if bstack11l1l11111l_opy_(pytest_version, bstack1ll1l1_opy_ (u"ࠥ࠼࠳࠷࠮࠲ࠤᮯ")) >= 0:
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠫ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮰")] = Module._register_setup_function_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠬࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮱")] = Module._register_setup_module_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"࠭ࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮲")] = Class._register_setup_class_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮳")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮴"))
            Module._register_setup_module_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᮵"))
            Class._register_setup_class_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᮶"))
            Class._register_setup_method_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮷"))
        else:
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮸")] = Module._inject_setup_function_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮹")] = Module._inject_setup_module_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᮺ")] = Class._inject_setup_class_fixture
            self._11l11ll1ll1_opy_[bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᮻ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᮼ"))
            Module._inject_setup_module_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮽ"))
            Class._inject_setup_class_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮾ"))
            Class._inject_setup_method_fixture = self.bstack11l11ll1111_opy_(bstack1ll1l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᮿ"))
    def bstack11l11ll11l1_opy_(self, bstack11l11ll1l11_opy_, hook_type):
        bstack11l11ll111l_opy_ = id(bstack11l11ll1l11_opy_.__class__)
        if (bstack11l11ll111l_opy_, hook_type) in self._11l11llll11_opy_:
            return
        meth = getattr(bstack11l11ll1l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11llll11_opy_[(bstack11l11ll111l_opy_, hook_type)] = meth
            setattr(bstack11l11ll1l11_opy_, hook_type, self.bstack11l11lll1ll_opy_(hook_type, bstack11l11ll111l_opy_))
    def bstack11l11llll1l_opy_(self, instance, bstack11l11ll1lll_opy_):
        if bstack11l11ll1lll_opy_ == bstack1ll1l1_opy_ (u"ࠨࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯀ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣᯁ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᯂ"))
        if bstack11l11ll1lll_opy_ == bstack1ll1l1_opy_ (u"ࠤࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᯃ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠤᯄ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࠨᯅ"))
        if bstack11l11ll1lll_opy_ == bstack1ll1l1_opy_ (u"ࠧࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠧᯆ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠦᯇ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠣᯈ"))
        if bstack11l11ll1lll_opy_ == bstack1ll1l1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯉ"):
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠣᯊ"))
            self.bstack11l11ll11l1_opy_(instance.obj, bstack1ll1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠧᯋ"))
    @staticmethod
    def bstack11l11lll111_opy_(hook_type, func, args):
        if hook_type in [bstack1ll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᯌ"), bstack1ll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᯍ")]:
            _11l11ll11ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11lll1ll_opy_(self, hook_type, bstack11l11ll111l_opy_):
        def bstack11l11lll1l1_opy_(arg=None):
            self.handler(hook_type, bstack1ll1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ᯎ"))
            result = None
            try:
                bstack11111l1l11_opy_ = self._11l11llll11_opy_[(bstack11l11ll111l_opy_, hook_type)]
                self.bstack11l11lll111_opy_(hook_type, bstack11111l1l11_opy_, (arg,))
                result = Result(result=bstack1ll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᯏ"))
            except Exception as e:
                result = Result(result=bstack1ll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᯐ"), exception=e)
                self.handler(hook_type, bstack1ll1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᯑ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᯒ"), result)
        def bstack11l11l1llll_opy_(this, arg=None):
            self.handler(hook_type, bstack1ll1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᯓ"))
            result = None
            exception = None
            try:
                self.bstack11l11lll111_opy_(hook_type, self._11l11llll11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᯔ"))
            except Exception as e:
                result = Result(result=bstack1ll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᯕ"), exception=e)
                self.handler(hook_type, bstack1ll1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᯖ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1ll1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᯗ"), result)
        if hook_type in [bstack1ll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᯘ"), bstack1ll1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᯙ")]:
            return bstack11l11l1llll_opy_
        return bstack11l11lll1l1_opy_
    def bstack11l11ll1111_opy_(self, bstack11l11ll1lll_opy_):
        def bstack11l11lll11l_opy_(this, *args, **kwargs):
            self.bstack11l11llll1l_opy_(this, bstack11l11ll1lll_opy_)
            self._11l11ll1ll1_opy_[bstack11l11ll1lll_opy_](this, *args, **kwargs)
        return bstack11l11lll11l_opy_