# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lll_opy_):
    global bstack1l11l11_opy_
    bstack1l1l1_opy_ = ord (bstack11lll_opy_ [-1])
    bstack1l111ll_opy_ = bstack11lll_opy_ [:-1]
    bstack11l_opy_ = bstack1l1l1_opy_ % len (bstack1l111ll_opy_)
    bstack11l111l_opy_ = bstack1l111ll_opy_ [:bstack11l_opy_] + bstack1l111ll_opy_ [bstack11l_opy_:]
    if bstack11111ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l_opy_)
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11lll11llll_opy_
from browserstack_sdk.bstack11l1llll11_opy_ import bstack11ll111l_opy_
def _11l1ll1l1ll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l1ll1ll1l_opy_:
    def __init__(self, handler):
        self._11l1lll111l_opy_ = {}
        self._11l1ll1llll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11ll111l_opy_.version()
        if bstack11lll11llll_opy_(pytest_version, bstack11l1l11_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᬠ")) >= 0:
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᬡ")] = Module._register_setup_function_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᬢ")] = Module._register_setup_module_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᬣ")] = Class._register_setup_class_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᬤ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᬥ"))
            Module._register_setup_module_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᬦ"))
            Class._register_setup_class_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᬧ"))
            Class._register_setup_method_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᬨ"))
        else:
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᬩ")] = Module._inject_setup_function_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᬪ")] = Module._inject_setup_module_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᬫ")] = Class._inject_setup_class_fixture
            self._11l1lll111l_opy_[bstack11l1l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᬬ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᬭ"))
            Module._inject_setup_module_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᬮ"))
            Class._inject_setup_class_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᬯ"))
            Class._inject_setup_method_fixture = self.bstack11l1ll1l111_opy_(bstack11l1l11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᬰ"))
    def bstack11l1lll11ll_opy_(self, bstack11l1lll11l1_opy_, hook_type):
        bstack11l1ll1l11l_opy_ = id(bstack11l1lll11l1_opy_.__class__)
        if (bstack11l1ll1l11l_opy_, hook_type) in self._11l1ll1llll_opy_:
            return
        meth = getattr(bstack11l1lll11l1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l1ll1llll_opy_[(bstack11l1ll1l11l_opy_, hook_type)] = meth
            setattr(bstack11l1lll11l1_opy_, hook_type, self.bstack11l1ll1l1l1_opy_(hook_type, bstack11l1ll1l11l_opy_))
    def bstack11l1ll1lll1_opy_(self, instance, bstack11l1ll11lll_opy_):
        if bstack11l1ll11lll_opy_ == bstack11l1l11_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᬱ"):
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᬲ"))
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᬳ"))
        if bstack11l1ll11lll_opy_ == bstack11l1l11_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫᬴ࠢ"):
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᬵ"))
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᬶ"))
        if bstack11l1ll11lll_opy_ == bstack11l1l11_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᬷ"):
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᬸ"))
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᬹ"))
        if bstack11l1ll11lll_opy_ == bstack11l1l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᬺ"):
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᬻ"))
            self.bstack11l1lll11ll_opy_(instance.obj, bstack11l1l11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᬼ"))
    @staticmethod
    def bstack11l1lll1ll1_opy_(hook_type, func, args):
        if hook_type in [bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᬽ"), bstack11l1l11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᬾ")]:
            _11l1ll1l1ll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l1ll1l1l1_opy_(self, hook_type, bstack11l1ll1l11l_opy_):
        def bstack11l1lll1111_opy_(arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᬿ"))
            result = None
            try:
                bstack1111111ll1_opy_ = self._11l1ll1llll_opy_[(bstack11l1ll1l11l_opy_, hook_type)]
                self.bstack11l1lll1ll1_opy_(hook_type, bstack1111111ll1_opy_, (arg,))
                result = Result(result=bstack11l1l11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᭀ"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᭁ"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᭂ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᭃ"), result)
        def bstack11l1lll1l1l_opy_(this, arg=None):
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨ᭄"))
            result = None
            exception = None
            try:
                self.bstack11l1lll1ll1_opy_(hook_type, self._11l1ll1llll_opy_[hook_type], (this, arg))
                result = Result(result=bstack11l1l11_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᭅ"))
            except Exception as e:
                result = Result(result=bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᭆ"), exception=e)
                self.handler(hook_type, bstack11l1l11_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᭇ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11l1l11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᭈ"), result)
        if hook_type in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᭉ"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᭊ")]:
            return bstack11l1lll1l1l_opy_
        return bstack11l1lll1111_opy_
    def bstack11l1ll1l111_opy_(self, bstack11l1ll11lll_opy_):
        def bstack11l1ll1ll11_opy_(this, *args, **kwargs):
            self.bstack11l1ll1lll1_opy_(this, bstack11l1ll11lll_opy_)
            self._11l1lll111l_opy_[bstack11l1ll11lll_opy_](this, *args, **kwargs)
        return bstack11l1ll1ll11_opy_