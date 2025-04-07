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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111lll111l_opy_ import RobotHandler
from bstack_utils.capture import bstack11l11111ll_opy_
from bstack_utils.bstack111lllll1l_opy_ import bstack111ll1l111_opy_, bstack11l111llll_opy_, bstack11l1111111_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack11l11l11_opy_
from bstack_utils.bstack11l111l1l1_opy_ import bstack11lll111l1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1llllllll1_opy_, bstack1ll11ll11_opy_, Result, \
    bstack111ll1l1l1_opy_, bstack111l1l1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧ༔"): [],
        bstack11l1l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ༕"): [],
        bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ༖"): []
    }
    bstack111llll111_opy_ = []
    bstack111l1ll11l_opy_ = []
    @staticmethod
    def bstack11l1111l1l_opy_(log):
        if not ((isinstance(log[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ༗")], list) or (isinstance(log[bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ༘")], dict)) and len(log[bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༙ࠩ")])>0) or (isinstance(log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༚")], str) and log[bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༛")].strip())):
            return
        active = bstack11l11l11_opy_.bstack11l111lll1_opy_()
        log = {
            bstack11l1l11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ༜"): log[bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ༝")],
            bstack11l1l11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ༞"): bstack111l1l1l11_opy_().isoformat() + bstack11l1l11_opy_ (u"࡛ࠧࠩ༟"),
            bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ༠"): log[bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༡")],
        }
        if active:
            if active[bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ༢")] == bstack11l1l11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ༣"):
                log[bstack11l1l11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༤")] = active[bstack11l1l11_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭༥")]
            elif active[bstack11l1l11_opy_ (u"ࠧࡵࡻࡳࡩࠬ༦")] == bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹ࠭༧"):
                log[bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ༨")] = active[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ༩")]
        bstack11lll111l1_opy_.bstack1lll1l1111_opy_([log])
    def __init__(self):
        self.messages = bstack111ll1ll11_opy_()
        self._111l1l11ll_opy_ = None
        self._111lll1l1l_opy_ = None
        self._111ll1l1ll_opy_ = OrderedDict()
        self.bstack11l1111l11_opy_ = bstack11l11111ll_opy_(self.bstack11l1111l1l_opy_)
    @bstack111ll1l1l1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l11l1_opy_()
        if not self._111ll1l1ll_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧ༪")), None):
            self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ༫"))] = {}
        bstack111lll11ll_opy_ = bstack11l1111111_opy_(
                bstack111l1llll1_opy_=attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ༬")),
                name=name,
                started_at=bstack1ll11ll11_opy_(),
                file_path=os.path.relpath(attrs[bstack11l1l11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ༭")], start=os.getcwd()) if attrs.get(bstack11l1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ༮")) != bstack11l1l11_opy_ (u"ࠩࠪ༯") else bstack11l1l11_opy_ (u"ࠪࠫ༰"),
                framework=bstack11l1l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ༱")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ༲"), None)
        self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ༳"))][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༴")] = bstack111lll11ll_opy_
    @bstack111ll1l1l1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111ll1llll_opy_()
        self._111l1lllll_opy_(messages)
        for bstack111llll1ll_opy_ in self.bstack111llll111_opy_:
            bstack111llll1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰ༵ࠪ")][bstack11l1l11_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ༶")].extend(self.store[bstack11l1l11_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴ༷ࠩ")])
            bstack11lll111l1_opy_.bstack1ll1l1l1ll_opy_(bstack111llll1ll_opy_)
        self.bstack111llll111_opy_ = []
        self.store[bstack11l1l11_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪ༸")] = []
    @bstack111ll1l1l1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l1111l11_opy_.start()
        if not self._111ll1l1ll_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠬ࡯ࡤࠨ༹")), None):
            self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ༺"))] = {}
        driver = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭༻"), None)
        bstack111lllll1l_opy_ = bstack11l1111111_opy_(
            bstack111l1llll1_opy_=attrs.get(bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫ༼")),
            name=name,
            started_at=bstack1ll11ll11_opy_(),
            file_path=os.path.relpath(attrs[bstack11l1l11_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༽")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1l111l_opy_(attrs.get(bstack11l1l11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ༾"), None)),
            framework=bstack11l1l11_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ༿"),
            tags=attrs[bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪཀ")],
            hooks=self.store[bstack11l1l11_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬཁ")],
            bstack11l111l11l_opy_=bstack11lll111l1_opy_.bstack11l11l111l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11l1l11_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤག").format(bstack11l1l11_opy_ (u"ࠣࠢࠥགྷ").join(attrs[bstack11l1l11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧང")]), name) if attrs[bstack11l1l11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨཅ")] else name
        )
        self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠫ࡮ࡪࠧཆ"))][bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨཇ")] = bstack111lllll1l_opy_
        threading.current_thread().current_test_uuid = bstack111lllll1l_opy_.bstack111ll11111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11l1l11_opy_ (u"࠭ࡩࡥࠩ཈"), None)
        self.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨཉ"), bstack111lllll1l_opy_)
    @bstack111ll1l1l1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l1111l11_opy_.reset()
        bstack111l11ll11_opy_ = bstack111lll11l1_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨཊ")), bstack11l1l11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪཋ"))
        self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ཌ"))][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཌྷ")].stop(time=bstack1ll11ll11_opy_(), duration=int(attrs.get(bstack11l1l11_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪཎ"), bstack11l1l11_opy_ (u"࠭࠰ࠨཏ"))), result=Result(result=bstack111l11ll11_opy_, exception=attrs.get(bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཐ")), bstack11l11l1l11_opy_=[attrs.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩད"))]))
        self.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫདྷ"), self._111ll1l1ll_opy_[attrs.get(bstack11l1l11_opy_ (u"ࠪ࡭ࡩ࠭ན"))][bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧཔ")], True)
        self.store[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩཕ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111ll1l1l1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l11l1_opy_()
        current_test_id = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨབ"), None)
        bstack111l1lll11_opy_ = current_test_id if bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩབྷ"), None) else bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫམ"), None)
        if attrs.get(bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧཙ"), bstack11l1l11_opy_ (u"ࠪࠫཚ")).lower() in [bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪཛ"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧཛྷ")]:
            hook_type = bstack111ll11lll_opy_(attrs.get(bstack11l1l11_opy_ (u"࠭ࡴࡺࡲࡨࠫཝ")), bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫཞ"), None))
            hook_name = bstack11l1l11_opy_ (u"ࠨࡽࢀࠫཟ").format(attrs.get(bstack11l1l11_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩའ"), bstack11l1l11_opy_ (u"ࠪࠫཡ")))
            if hook_type in [bstack11l1l11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨར"), bstack11l1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨལ")]:
                hook_name = bstack11l1l11_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧཤ").format(bstack111lll1lll_opy_.get(hook_type), attrs.get(bstack11l1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧཥ"), bstack11l1l11_opy_ (u"ࠨࠩས")))
            bstack111l1l1lll_opy_ = bstack11l111llll_opy_(
                bstack111l1llll1_opy_=bstack111l1lll11_opy_ + bstack11l1l11_opy_ (u"ࠩ࠰ࠫཧ") + attrs.get(bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨཨ"), bstack11l1l11_opy_ (u"ࠫࠬཀྵ")).lower(),
                name=hook_name,
                started_at=bstack1ll11ll11_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11l1l11_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཪ")), start=os.getcwd()),
                framework=bstack11l1l11_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཫ"),
                tags=attrs[bstack11l1l11_opy_ (u"ࠧࡵࡣࡪࡷࠬཬ")],
                scope=RobotHandler.bstack111l1l111l_opy_(attrs.get(bstack11l1l11_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ཭"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111l1l1lll_opy_.bstack111ll11111_opy_()
            threading.current_thread().current_hook_id = bstack111l1lll11_opy_ + bstack11l1l11_opy_ (u"ࠩ࠰ࠫ཮") + attrs.get(bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨ཯"), bstack11l1l11_opy_ (u"ࠫࠬ཰")).lower()
            self.store[bstack11l1l11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥཱࠩ")] = [bstack111l1l1lll_opy_.bstack111ll11111_opy_()]
            if bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦིࠪ"), None):
                self.store[bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶཱིࠫ")].append(bstack111l1l1lll_opy_.bstack111ll11111_opy_())
            else:
                self.store[bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹུࠧ")].append(bstack111l1l1lll_opy_.bstack111ll11111_opy_())
            if bstack111l1lll11_opy_:
                self._111ll1l1ll_opy_[bstack111l1lll11_opy_ + bstack11l1l11_opy_ (u"ࠩ࠰ཱུࠫ") + attrs.get(bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨྲྀ"), bstack11l1l11_opy_ (u"ࠫࠬཷ")).lower()] = { bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨླྀ"): bstack111l1l1lll_opy_ }
            bstack11lll111l1_opy_.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧཹ"), bstack111l1l1lll_opy_)
        else:
            bstack11l1111ll1_opy_ = {
                bstack11l1l11_opy_ (u"ࠧࡪࡦེࠪ"): uuid4().__str__(),
                bstack11l1l11_opy_ (u"ࠨࡶࡨࡼࡹཻ࠭"): bstack11l1l11_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨོ").format(attrs.get(bstack11l1l11_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧཽࠪ")), attrs.get(bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩཾ"), bstack11l1l11_opy_ (u"ࠬ࠭ཿ"))) if attrs.get(bstack11l1l11_opy_ (u"࠭ࡡࡳࡩࡶྀࠫ"), []) else attrs.get(bstack11l1l11_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ཱྀࠧ")),
                bstack11l1l11_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨྂ"): attrs.get(bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧྃ"), []),
                bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ྄ࠧ"): bstack1ll11ll11_opy_(),
                bstack11l1l11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ྅"): bstack11l1l11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭྆"),
                bstack11l1l11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ྇"): attrs.get(bstack11l1l11_opy_ (u"ࠧࡥࡱࡦࠫྈ"), bstack11l1l11_opy_ (u"ࠨࠩྉ"))
            }
            if attrs.get(bstack11l1l11_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪྊ"), bstack11l1l11_opy_ (u"ࠪࠫྋ")) != bstack11l1l11_opy_ (u"ࠫࠬྌ"):
                bstack11l1111ll1_opy_[bstack11l1l11_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ྍ")] = attrs.get(bstack11l1l11_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧྎ"))
            if not self.bstack111l1ll11l_opy_:
                self._111ll1l1ll_opy_[self._111lll1ll1_opy_()][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྏ")].add_step(bstack11l1111ll1_opy_)
                threading.current_thread().current_step_uuid = bstack11l1111ll1_opy_[bstack11l1l11_opy_ (u"ࠨ࡫ࡧࠫྐ")]
            self.bstack111l1ll11l_opy_.append(bstack11l1111ll1_opy_)
    @bstack111ll1l1l1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111ll1llll_opy_()
        self._111l1lllll_opy_(messages)
        current_test_id = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫྑ"), None)
        bstack111l1lll11_opy_ = current_test_id if current_test_id else bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ྒ"), None)
        bstack111ll1111l_opy_ = bstack111lll11l1_opy_.get(attrs.get(bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫྒྷ")), bstack11l1l11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ྔ"))
        bstack111l1ll1ll_opy_ = attrs.get(bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྕ"))
        if bstack111ll1111l_opy_ != bstack11l1l11_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྖ") and not attrs.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྗ")) and self._111l1l11ll_opy_:
            bstack111l1ll1ll_opy_ = self._111l1l11ll_opy_
        bstack11l111111l_opy_ = Result(result=bstack111ll1111l_opy_, exception=bstack111l1ll1ll_opy_, bstack11l11l1l11_opy_=[bstack111l1ll1ll_opy_])
        if attrs.get(bstack11l1l11_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ྘"), bstack11l1l11_opy_ (u"ࠪࠫྙ")).lower() in [bstack11l1l11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪྚ"), bstack11l1l11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧྛ")]:
            bstack111l1lll11_opy_ = current_test_id if current_test_id else bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩྜ"), None)
            if bstack111l1lll11_opy_:
                bstack11l111l111_opy_ = bstack111l1lll11_opy_ + bstack11l1l11_opy_ (u"ࠢ࠮ࠤྜྷ") + attrs.get(bstack11l1l11_opy_ (u"ࠨࡶࡼࡴࡪ࠭ྞ"), bstack11l1l11_opy_ (u"ࠩࠪྟ")).lower()
                self._111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྠ")].stop(time=bstack1ll11ll11_opy_(), duration=int(attrs.get(bstack11l1l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྡ"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧྡྷ"))), result=bstack11l111111l_opy_)
                bstack11lll111l1_opy_.bstack111lllllll_opy_(bstack11l1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨྣ"), self._111ll1l1ll_opy_[bstack11l111l111_opy_][bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪྤ")])
        else:
            bstack111l1lll11_opy_ = current_test_id if current_test_id else bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪྥ"), None)
            if bstack111l1lll11_opy_ and len(self.bstack111l1ll11l_opy_) == 1:
                current_step_uuid = bstack1llllllll1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ྦ"), None)
                self._111ll1l1ll_opy_[bstack111l1lll11_opy_][bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ྦྷ")].bstack11l11l1l1l_opy_(current_step_uuid, duration=int(attrs.get(bstack11l1l11_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩྨ"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧྩ"))), result=bstack11l111111l_opy_)
            else:
                self.bstack111lll1l11_opy_(attrs)
            self.bstack111l1ll11l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11l1l11_opy_ (u"࠭ࡨࡵ࡯࡯ࠫྪ"), bstack11l1l11_opy_ (u"ࠧ࡯ࡱࠪྫ")) == bstack11l1l11_opy_ (u"ࠨࡻࡨࡷࠬྫྷ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l11l11_opy_.bstack11l111lll1_opy_():
                logs.append({
                    bstack11l1l11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬྭ"): bstack1ll11ll11_opy_(),
                    bstack11l1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྮ"): message.get(bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬྯ")),
                    bstack11l1l11_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫྰ"): message.get(bstack11l1l11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬྱ")),
                    **bstack11l11l11_opy_.bstack11l111lll1_opy_()
                })
                if len(logs) > 0:
                    bstack11lll111l1_opy_.bstack1lll1l1111_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack11lll111l1_opy_.bstack111l1l1ll1_opy_()
    def bstack111lll1l11_opy_(self, bstack111ll11l11_opy_):
        if not bstack11l11l11_opy_.bstack11l111lll1_opy_():
            return
        kwname = bstack11l1l11_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ྲ").format(bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨླ")), bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧྴ"), bstack11l1l11_opy_ (u"ࠪࠫྵ"))) if bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠫࡦࡸࡧࡴࠩྶ"), []) else bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬྷ"))
        error_message = bstack11l1l11_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧྸ").format(kwname, bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྐྵ")), str(bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྺ"))))
        bstack111llll11l_opy_ = bstack11l1l11_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣྻ").format(kwname, bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪྼ")))
        bstack111lll1111_opy_ = error_message if bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ྽")) else bstack111llll11l_opy_
        bstack111l1ll111_opy_ = {
            bstack11l1l11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ྾"): self.bstack111l1ll11l_opy_[-1].get(bstack11l1l11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ྿"), bstack1ll11ll11_opy_()),
            bstack11l1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿀"): bstack111lll1111_opy_,
            bstack11l1l11_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿁"): bstack11l1l11_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ࿂") if bstack111ll11l11_opy_.get(bstack11l1l11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ࿃")) == bstack11l1l11_opy_ (u"ࠫࡋࡇࡉࡍࠩ࿄") else bstack11l1l11_opy_ (u"ࠬࡏࡎࡇࡑࠪ࿅"),
            **bstack11l11l11_opy_.bstack11l111lll1_opy_()
        }
        bstack11lll111l1_opy_.bstack1lll1l1111_opy_([bstack111l1ll111_opy_])
    def _111lll1ll1_opy_(self):
        for bstack111l1llll1_opy_ in reversed(self._111ll1l1ll_opy_):
            bstack111l1lll1l_opy_ = bstack111l1llll1_opy_
            data = self._111ll1l1ll_opy_[bstack111l1llll1_opy_][bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ࿆ࠩ")]
            if isinstance(data, bstack11l111llll_opy_):
                if not bstack11l1l11_opy_ (u"ࠧࡆࡃࡆࡌࠬ࿇") in data.bstack111l11llll_opy_():
                    return bstack111l1lll1l_opy_
            else:
                return bstack111l1lll1l_opy_
    def _111l1lllll_opy_(self, messages):
        try:
            bstack111ll1lll1_opy_ = BuiltIn().get_variable_value(bstack11l1l11_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢ࿈")) in (bstack111ll111ll_opy_.DEBUG, bstack111ll111ll_opy_.TRACE)
            for message, bstack111l1ll1l1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11l1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿉"))
                level = message.get(bstack11l1l11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿊"))
                if level == bstack111ll111ll_opy_.FAIL:
                    self._111l1l11ll_opy_ = name or self._111l1l11ll_opy_
                    self._111lll1l1l_opy_ = bstack111l1ll1l1_opy_.get(bstack11l1l11_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ࿋")) if bstack111ll1lll1_opy_ and bstack111l1ll1l1_opy_ else self._111lll1l1l_opy_
        except:
            pass
    @classmethod
    def bstack111lllllll_opy_(self, event: str, bstack111ll1ll1l_opy_: bstack111ll1l111_opy_, bstack111l1l1l1l_opy_=False):
        if event == bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ࿌"):
            bstack111ll1ll1l_opy_.set(hooks=self.store[bstack11l1l11_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ࿍")])
        if event == bstack11l1l11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ࿎"):
            event = bstack11l1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ࿏")
        if bstack111l1l1l1l_opy_:
            bstack111ll11ll1_opy_ = {
                bstack11l1l11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭࿐"): event,
                bstack111ll1ll1l_opy_.bstack111ll111l1_opy_(): bstack111ll1ll1l_opy_.bstack111llll1l1_opy_(event)
            }
            self.bstack111llll111_opy_.append(bstack111ll11ll1_opy_)
        else:
            bstack11lll111l1_opy_.bstack111lllllll_opy_(event, bstack111ll1ll1l_opy_)
class bstack111ll1ll11_opy_:
    def __init__(self):
        self._111ll1l11l_opy_ = []
    def bstack111l1l11l1_opy_(self):
        self._111ll1l11l_opy_.append([])
    def bstack111ll1llll_opy_(self):
        return self._111ll1l11l_opy_.pop() if self._111ll1l11l_opy_ else list()
    def push(self, message):
        self._111ll1l11l_opy_[-1].append(message) if self._111ll1l11l_opy_ else self._111ll1l11l_opy_.append([message])
class bstack111ll111ll_opy_:
    FAIL = bstack11l1l11_opy_ (u"ࠪࡊࡆࡏࡌࠨ࿑")
    ERROR = bstack11l1l11_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿒")
    WARNING = bstack11l1l11_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ࿓")
    bstack111ll11l1l_opy_ = bstack11l1l11_opy_ (u"࠭ࡉࡏࡈࡒࠫ࿔")
    DEBUG = bstack11l1l11_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭࿕")
    TRACE = bstack11l1l11_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧ࿖")
    bstack111l1l1111_opy_ = [FAIL, ERROR]
def bstack111l11ll1l_opy_(bstack111l11lll1_opy_):
    if not bstack111l11lll1_opy_:
        return None
    if bstack111l11lll1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ࿗"), None):
        return getattr(bstack111l11lll1_opy_[bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭࿘")], bstack11l1l11_opy_ (u"ࠫࡺࡻࡩࡥࠩ࿙"), None)
    return bstack111l11lll1_opy_.get(bstack11l1l11_opy_ (u"ࠬࡻࡵࡪࡦࠪ࿚"), None)
def bstack111ll11lll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11l1l11_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ࿛"), bstack11l1l11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ࿜")]:
        return
    if hook_type.lower() == bstack11l1l11_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿝"):
        if current_test_uuid is None:
            return bstack11l1l11_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭࿞")
        else:
            return bstack11l1l11_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ࿟")
    elif hook_type.lower() == bstack11l1l11_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭࿠"):
        if current_test_uuid is None:
            return bstack11l1l11_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨ࿡")
        else:
            return bstack11l1l11_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ࿢")