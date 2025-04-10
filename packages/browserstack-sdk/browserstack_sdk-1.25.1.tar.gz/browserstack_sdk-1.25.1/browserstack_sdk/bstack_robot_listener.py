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
import os
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack111l11l1l1_opy_ import RobotHandler
from bstack_utils.capture import bstack11l111l1l1_opy_
from bstack_utils.bstack11l111l1ll_opy_ import bstack111lll1ll1_opy_, bstack11l11l111l_opy_, bstack11l11111l1_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11l1ll1ll_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11111l111_opy_, bstack11l1ll11ll_opy_, Result, \
    bstack111ll11ll1_opy_, bstack111l1l1ll1_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ༖"): [],
        bstack1ll1l1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༗"): [],
        bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶ༘ࠫ"): []
    }
    bstack111lll1111_opy_ = []
    bstack111l11ll1l_opy_ = []
    @staticmethod
    def bstack11l11l1111_opy_(log):
        if not ((isinstance(log[bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ༙ࠩ")], list) or (isinstance(log[bstack1ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ༚")], dict)) and len(log[bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༛")])>0) or (isinstance(log[bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༜")], str) and log[bstack1ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭༝")].strip())):
            return
        active = bstack11l1ll1ll_opy_.bstack11l111ll11_opy_()
        log = {
            bstack1ll1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ༞"): log[bstack1ll1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭༟")],
            bstack1ll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ༠"): bstack111l1l1ll1_opy_().isoformat() + bstack1ll1l1_opy_ (u"ࠩ࡝ࠫ༡"),
            bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ༢"): log[bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ༣")],
        }
        if active:
            if active[bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ༤")] == bstack1ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ༥"):
                log[bstack1ll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ༦")] = active[bstack1ll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ༧")]
            elif active[bstack1ll1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ༨")] == bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨ༩"):
                log[bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ༪")] = active[bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ༫")]
        bstack1l1lll1lll_opy_.bstack1l111lll1_opy_([log])
    def __init__(self):
        self.messages = bstack111ll1l11l_opy_()
        self._111l1lll11_opy_ = None
        self._111lll1lll_opy_ = None
        self._111l11l11l_opy_ = OrderedDict()
        self.bstack11l11111ll_opy_ = bstack11l111l1l1_opy_(self.bstack11l11l1111_opy_)
    @bstack111ll11ll1_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack111l1l1111_opy_()
        if not self._111l11l11l_opy_.get(attrs.get(bstack1ll1l1_opy_ (u"࠭ࡩࡥࠩ༬")), None):
            self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"ࠧࡪࡦࠪ༭"))] = {}
        bstack111l1l11l1_opy_ = bstack11l11111l1_opy_(
                bstack111l1ll1l1_opy_=attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫ༮")),
                name=name,
                started_at=bstack11l1ll11ll_opy_(),
                file_path=os.path.relpath(attrs[bstack1ll1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༯")], start=os.getcwd()) if attrs.get(bstack1ll1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ༰")) != bstack1ll1l1_opy_ (u"ࠫࠬ༱") else bstack1ll1l1_opy_ (u"ࠬ࠭༲"),
                framework=bstack1ll1l1_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬ༳")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1ll1l1_opy_ (u"ࠧࡪࡦࠪ༴"), None)
        self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡫ࡧ༵ࠫ"))][bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ༶")] = bstack111l1l11l1_opy_
    @bstack111ll11ll1_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack111l1l111l_opy_()
        self._111l1llll1_opy_(messages)
        for bstack111ll11lll_opy_ in self.bstack111lll1111_opy_:
            bstack111ll11lll_opy_[bstack1ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲ༷ࠬ")][bstack1ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ༸")].extend(self.store[bstack1ll1l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶ༹ࠫ")])
            bstack1l1lll1lll_opy_.bstack1l111l1ll_opy_(bstack111ll11lll_opy_)
        self.bstack111lll1111_opy_ = []
        self.store[bstack1ll1l1_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ༺")] = []
    @bstack111ll11ll1_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11l11111ll_opy_.start()
        if not self._111l11l11l_opy_.get(attrs.get(bstack1ll1l1_opy_ (u"ࠧࡪࡦࠪ༻")), None):
            self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫ༼"))] = {}
        driver = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ༽"), None)
        bstack11l111l1ll_opy_ = bstack11l11111l1_opy_(
            bstack111l1ll1l1_opy_=attrs.get(bstack1ll1l1_opy_ (u"ࠪ࡭ࡩ࠭༾")),
            name=name,
            started_at=bstack11l1ll11ll_opy_(),
            file_path=os.path.relpath(attrs[bstack1ll1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ༿")], start=os.getcwd()),
            scope=RobotHandler.bstack111l1l1l1l_opy_(attrs.get(bstack1ll1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬཀ"), None)),
            framework=bstack1ll1l1_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬཁ"),
            tags=attrs[bstack1ll1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬག")],
            hooks=self.store[bstack1ll1l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧགྷ")],
            bstack11l111llll_opy_=bstack1l1lll1lll_opy_.bstack11l111ll1l_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1ll1l1_opy_ (u"ࠤࡾࢁࠥࡢ࡮ࠡࡽࢀࠦང").format(bstack1ll1l1_opy_ (u"ࠥࠤࠧཅ").join(attrs[bstack1ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩཆ")]), name) if attrs[bstack1ll1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪཇ")] else name
        )
        self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"࠭ࡩࡥࠩ཈"))][bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪཉ")] = bstack11l111l1ll_opy_
        threading.current_thread().current_test_uuid = bstack11l111l1ll_opy_.bstack111ll11111_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡫ࡧࠫཊ"), None)
        self.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪཋ"), bstack11l111l1ll_opy_)
    @bstack111ll11ll1_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11l11111ll_opy_.reset()
        bstack111lll11l1_opy_ = bstack111l1ll1ll_opy_.get(attrs.get(bstack1ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪཌ")), bstack1ll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬཌྷ"))
        self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"ࠬ࡯ࡤࠨཎ"))][bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩཏ")].stop(time=bstack11l1ll11ll_opy_(), duration=int(attrs.get(bstack1ll1l1_opy_ (u"ࠧࡦ࡮ࡤࡴࡸ࡫ࡤࡵ࡫ࡰࡩࠬཐ"), bstack1ll1l1_opy_ (u"ࠨ࠲ࠪད"))), result=Result(result=bstack111lll11l1_opy_, exception=attrs.get(bstack1ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪདྷ")), bstack11l1111lll_opy_=[attrs.get(bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫན"))]))
        self.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭པ"), self._111l11l11l_opy_[attrs.get(bstack1ll1l1_opy_ (u"ࠬ࡯ࡤࠨཕ"))][bstack1ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩབ")], True)
        self.store[bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫབྷ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack111ll11ll1_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack111l1l1111_opy_()
        current_test_id = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡦࠪམ"), None)
        bstack111ll1llll_opy_ = current_test_id if bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫཙ"), None) else bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ཚ"), None)
        if attrs.get(bstack1ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩཛ"), bstack1ll1l1_opy_ (u"ࠬ࠭ཛྷ")).lower() in [bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬཝ"), bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩཞ")]:
            hook_type = bstack111ll111l1_opy_(attrs.get(bstack1ll1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ཟ")), bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭འ"), None))
            hook_name = bstack1ll1l1_opy_ (u"ࠪࡿࢂ࠭ཡ").format(attrs.get(bstack1ll1l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫར"), bstack1ll1l1_opy_ (u"ࠬ࠭ལ")))
            if hook_type in [bstack1ll1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪཤ"), bstack1ll1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪཥ")]:
                hook_name = bstack1ll1l1_opy_ (u"ࠨ࡝ࡾࢁࡢࠦࡻࡾࠩས").format(bstack111llll111_opy_.get(hook_type), attrs.get(bstack1ll1l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩཧ"), bstack1ll1l1_opy_ (u"ࠪࠫཨ")))
            bstack111lll1l11_opy_ = bstack11l11l111l_opy_(
                bstack111l1ll1l1_opy_=bstack111ll1llll_opy_ + bstack1ll1l1_opy_ (u"ࠫ࠲࠭ཀྵ") + attrs.get(bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪཪ"), bstack1ll1l1_opy_ (u"࠭ࠧཫ")).lower(),
                name=hook_name,
                started_at=bstack11l1ll11ll_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1ll1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧཬ")), start=os.getcwd()),
                framework=bstack1ll1l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ཭"),
                tags=attrs[bstack1ll1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ཮")],
                scope=RobotHandler.bstack111l1l1l1l_opy_(attrs.get(bstack1ll1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ཯"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack111lll1l11_opy_.bstack111ll11111_opy_()
            threading.current_thread().current_hook_id = bstack111ll1llll_opy_ + bstack1ll1l1_opy_ (u"ࠫ࠲࠭཰") + attrs.get(bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧཱࠪ"), bstack1ll1l1_opy_ (u"ི࠭ࠧ")).lower()
            self.store[bstack1ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧཱིࠫ")] = [bstack111lll1l11_opy_.bstack111ll11111_opy_()]
            if bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨུࠬ"), None):
                self.store[bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸཱུ࠭")].append(bstack111lll1l11_opy_.bstack111ll11111_opy_())
            else:
                self.store[bstack1ll1l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩྲྀ")].append(bstack111lll1l11_opy_.bstack111ll11111_opy_())
            if bstack111ll1llll_opy_:
                self._111l11l11l_opy_[bstack111ll1llll_opy_ + bstack1ll1l1_opy_ (u"ࠫ࠲࠭ཷ") + attrs.get(bstack1ll1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪླྀ"), bstack1ll1l1_opy_ (u"࠭ࠧཹ")).lower()] = { bstack1ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣེࠪ"): bstack111lll1l11_opy_ }
            bstack1l1lll1lll_opy_.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥཻࠩ"), bstack111lll1l11_opy_)
        else:
            bstack111lllll11_opy_ = {
                bstack1ll1l1_opy_ (u"ࠩ࡬ࡨོࠬ"): uuid4().__str__(),
                bstack1ll1l1_opy_ (u"ࠪࡸࡪࡾࡴࠨཽ"): bstack1ll1l1_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪཾ").format(attrs.get(bstack1ll1l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬཿ")), attrs.get(bstack1ll1l1_opy_ (u"࠭ࡡࡳࡩࡶྀࠫ"), bstack1ll1l1_opy_ (u"ࠧࠨཱྀ"))) if attrs.get(bstack1ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྂ"), []) else attrs.get(bstack1ll1l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩྃ")),
                bstack1ll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡠࡣࡵ࡫ࡺࡳࡥ࡯ࡶ྄ࠪ"): attrs.get(bstack1ll1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩ྅"), []),
                bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ྆"): bstack11l1ll11ll_opy_(),
                bstack1ll1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭྇"): bstack1ll1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨྈ"),
                bstack1ll1l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྉ"): attrs.get(bstack1ll1l1_opy_ (u"ࠩࡧࡳࡨ࠭ྊ"), bstack1ll1l1_opy_ (u"ࠪࠫྋ"))
            }
            if attrs.get(bstack1ll1l1_opy_ (u"ࠫࡱ࡯ࡢ࡯ࡣࡰࡩࠬྌ"), bstack1ll1l1_opy_ (u"ࠬ࠭ྍ")) != bstack1ll1l1_opy_ (u"࠭ࠧྎ"):
                bstack111lllll11_opy_[bstack1ll1l1_opy_ (u"ࠧ࡬ࡧࡼࡻࡴࡸࡤࠨྏ")] = attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡮࡬ࡦࡳࡧ࡭ࡦࠩྐ"))
            if not self.bstack111l11ll1l_opy_:
                self._111l11l11l_opy_[self._111l1ll111_opy_()][bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྑ")].add_step(bstack111lllll11_opy_)
                threading.current_thread().current_step_uuid = bstack111lllll11_opy_[bstack1ll1l1_opy_ (u"ࠪ࡭ࡩ࠭ྒ")]
            self.bstack111l11ll1l_opy_.append(bstack111lllll11_opy_)
    @bstack111ll11ll1_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack111l1l111l_opy_()
        self._111l1llll1_opy_(messages)
        current_test_id = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ྒྷ"), None)
        bstack111ll1llll_opy_ = current_test_id if current_test_id else bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨྔ"), None)
        bstack111l1l1lll_opy_ = bstack111l1ll1ll_opy_.get(attrs.get(bstack1ll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྕ")), bstack1ll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨྖ"))
        bstack111ll1lll1_opy_ = attrs.get(bstack1ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྗ"))
        if bstack111l1l1lll_opy_ != bstack1ll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ྘") and not attrs.get(bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྙ")) and self._111l1lll11_opy_:
            bstack111ll1lll1_opy_ = self._111l1lll11_opy_
        bstack11l1111l1l_opy_ = Result(result=bstack111l1l1lll_opy_, exception=bstack111ll1lll1_opy_, bstack11l1111lll_opy_=[bstack111ll1lll1_opy_])
        if attrs.get(bstack1ll1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩྚ"), bstack1ll1l1_opy_ (u"ࠬ࠭ྛ")).lower() in [bstack1ll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬྜ"), bstack1ll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩྜྷ")]:
            bstack111ll1llll_opy_ = current_test_id if current_test_id else bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫྞ"), None)
            if bstack111ll1llll_opy_:
                bstack11l111l11l_opy_ = bstack111ll1llll_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠰ࠦྟ") + attrs.get(bstack1ll1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨྠ"), bstack1ll1l1_opy_ (u"ࠫࠬྡ")).lower()
                self._111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྡྷ")].stop(time=bstack11l1ll11ll_opy_(), duration=int(attrs.get(bstack1ll1l1_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫྣ"), bstack1ll1l1_opy_ (u"ࠧ࠱ࠩྤ"))), result=bstack11l1111l1l_opy_)
                bstack1l1lll1lll_opy_.bstack11l11l11l1_opy_(bstack1ll1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪྥ"), self._111l11l11l_opy_[bstack11l111l11l_opy_][bstack1ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬྦ")])
        else:
            bstack111ll1llll_opy_ = current_test_id if current_test_id else bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡ࡬ࡨࠬྦྷ"), None)
            if bstack111ll1llll_opy_ and len(self.bstack111l11ll1l_opy_) == 1:
                current_step_uuid = bstack11111l111_opy_(threading.current_thread(), bstack1ll1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡹࡴࡦࡲࡢࡹࡺ࡯ࡤࠨྨ"), None)
                self._111l11l11l_opy_[bstack111ll1llll_opy_][bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨྩ")].bstack111llll11l_opy_(current_step_uuid, duration=int(attrs.get(bstack1ll1l1_opy_ (u"࠭ࡥ࡭ࡣࡳࡷࡪࡪࡴࡪ࡯ࡨࠫྪ"), bstack1ll1l1_opy_ (u"ࠧ࠱ࠩྫ"))), result=bstack11l1111l1l_opy_)
            else:
                self.bstack111ll1l1l1_opy_(attrs)
            self.bstack111l11ll1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1ll1l1_opy_ (u"ࠨࡪࡷࡱࡱ࠭ྫྷ"), bstack1ll1l1_opy_ (u"ࠩࡱࡳࠬྭ")) == bstack1ll1l1_opy_ (u"ࠪࡽࡪࡹࠧྮ"):
                return
            self.messages.push(message)
            logs = []
            if bstack11l1ll1ll_opy_.bstack11l111ll11_opy_():
                logs.append({
                    bstack1ll1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧྯ"): bstack11l1ll11ll_opy_(),
                    bstack1ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ྰ"): message.get(bstack1ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྱ")),
                    bstack1ll1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ྲ"): message.get(bstack1ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧླ")),
                    **bstack11l1ll1ll_opy_.bstack11l111ll11_opy_()
                })
                if len(logs) > 0:
                    bstack1l1lll1lll_opy_.bstack1l111lll1_opy_(logs)
        except Exception as err:
            pass
    def close(self):
        bstack1l1lll1lll_opy_.bstack111ll11l11_opy_()
    def bstack111ll1l1l1_opy_(self, bstack111l1ll11l_opy_):
        if not bstack11l1ll1ll_opy_.bstack11l111ll11_opy_():
            return
        kwname = bstack1ll1l1_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨྴ").format(bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪྵ")), bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩྶ"), bstack1ll1l1_opy_ (u"ࠬ࠭ྷ"))) if bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫྸ"), []) else bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧྐྵ"))
        error_message = bstack1ll1l1_opy_ (u"ࠣ࡭ࡺࡲࡦࡳࡥ࠻ࠢ࡟ࠦࢀ࠶ࡽ࡝ࠤࠣࢀࠥࡹࡴࡢࡶࡸࡷ࠿ࠦ࡜ࠣࡽ࠴ࢁࡡࠨࠠࡽࠢࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦ࡜ࠣࡽ࠵ࢁࡡࠨࠢྺ").format(kwname, bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩྻ")), str(bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྼ"))))
        bstack111l11lll1_opy_ = bstack1ll1l1_opy_ (u"ࠦࡰࡽ࡮ࡢ࡯ࡨ࠾ࠥࡢࠢࡼ࠲ࢀࡠࠧࠦࡼࠡࡵࡷࡥࡹࡻࡳ࠻ࠢ࡟ࠦࢀ࠷ࡽ࡝ࠤࠥ྽").format(kwname, bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ྾")))
        bstack111ll1ll1l_opy_ = error_message if bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ྿")) else bstack111l11lll1_opy_
        bstack111ll1l111_opy_ = {
            bstack1ll1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ࿀"): self.bstack111l11ll1l_opy_[-1].get(bstack1ll1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ࿁"), bstack11l1ll11ll_opy_()),
            bstack1ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ࿂"): bstack111ll1ll1l_opy_,
            bstack1ll1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ࿃"): bstack1ll1l1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ࿄") if bstack111l1ll11l_opy_.get(bstack1ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ࿅")) == bstack1ll1l1_opy_ (u"࠭ࡆࡂࡋࡏ࿆ࠫ") else bstack1ll1l1_opy_ (u"ࠧࡊࡐࡉࡓࠬ࿇"),
            **bstack11l1ll1ll_opy_.bstack11l111ll11_opy_()
        }
        bstack1l1lll1lll_opy_.bstack1l111lll1_opy_([bstack111ll1l111_opy_])
    def _111l1ll111_opy_(self):
        for bstack111l1ll1l1_opy_ in reversed(self._111l11l11l_opy_):
            bstack111l1l11ll_opy_ = bstack111l1ll1l1_opy_
            data = self._111l11l11l_opy_[bstack111l1ll1l1_opy_][bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ࿈")]
            if isinstance(data, bstack11l11l111l_opy_):
                if not bstack1ll1l1_opy_ (u"ࠩࡈࡅࡈࡎࠧ࿉") in data.bstack111ll1ll11_opy_():
                    return bstack111l1l11ll_opy_
            else:
                return bstack111l1l11ll_opy_
    def _111l1llll1_opy_(self, messages):
        try:
            bstack111l1lllll_opy_ = BuiltIn().get_variable_value(bstack1ll1l1_opy_ (u"ࠥࠨࢀࡒࡏࡈࠢࡏࡉ࡛ࡋࡌࡾࠤ࿊")) in (bstack111ll111ll_opy_.DEBUG, bstack111ll111ll_opy_.TRACE)
            for message, bstack111lll11ll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ࿋"))
                level = message.get(bstack1ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿌"))
                if level == bstack111ll111ll_opy_.FAIL:
                    self._111l1lll11_opy_ = name or self._111l1lll11_opy_
                    self._111lll1lll_opy_ = bstack111lll11ll_opy_.get(bstack1ll1l1_opy_ (u"ࠨ࡭ࡦࡵࡶࡥ࡬࡫ࠢ࿍")) if bstack111l1lllll_opy_ and bstack111lll11ll_opy_ else self._111lll1lll_opy_
        except:
            pass
    @classmethod
    def bstack11l11l11l1_opy_(self, event: str, bstack111lll111l_opy_: bstack111lll1ll1_opy_, bstack111l1l1l11_opy_=False):
        if event == bstack1ll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ࿎"):
            bstack111lll111l_opy_.set(hooks=self.store[bstack1ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬ࿏")])
        if event == bstack1ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪ࿐"):
            event = bstack1ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ࿑")
        if bstack111l1l1l11_opy_:
            bstack111ll1l1ll_opy_ = {
                bstack1ll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ࿒"): event,
                bstack111lll111l_opy_.bstack111l11llll_opy_(): bstack111lll111l_opy_.bstack111ll11l1l_opy_(event)
            }
            self.bstack111lll1111_opy_.append(bstack111ll1l1ll_opy_)
        else:
            bstack1l1lll1lll_opy_.bstack11l11l11l1_opy_(event, bstack111lll111l_opy_)
class bstack111ll1l11l_opy_:
    def __init__(self):
        self._111l11l1ll_opy_ = []
    def bstack111l1l1111_opy_(self):
        self._111l11l1ll_opy_.append([])
    def bstack111l1l111l_opy_(self):
        return self._111l11l1ll_opy_.pop() if self._111l11l1ll_opy_ else list()
    def push(self, message):
        self._111l11l1ll_opy_[-1].append(message) if self._111l11l1ll_opy_ else self._111l11l1ll_opy_.append([message])
class bstack111ll111ll_opy_:
    FAIL = bstack1ll1l1_opy_ (u"ࠬࡌࡁࡊࡎࠪ࿓")
    ERROR = bstack1ll1l1_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬ࿔")
    WARNING = bstack1ll1l1_opy_ (u"ࠧࡘࡃࡕࡒࠬ࿕")
    bstack111ll1111l_opy_ = bstack1ll1l1_opy_ (u"ࠨࡋࡑࡊࡔ࠭࿖")
    DEBUG = bstack1ll1l1_opy_ (u"ࠩࡇࡉࡇ࡛ࡇࠨ࿗")
    TRACE = bstack1ll1l1_opy_ (u"ࠪࡘࡗࡇࡃࡆࠩ࿘")
    bstack111l11ll11_opy_ = [FAIL, ERROR]
def bstack111lll1l1l_opy_(bstack111l1lll1l_opy_):
    if not bstack111l1lll1l_opy_:
        return None
    if bstack111l1lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࿙"), None):
        return getattr(bstack111l1lll1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ࿚")], bstack1ll1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ࿛"), None)
    return bstack111l1lll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ࿜"), None)
def bstack111ll111l1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1ll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ࿝"), bstack1ll1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ࿞")]:
        return
    if hook_type.lower() == bstack1ll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ࿟"):
        if current_test_uuid is None:
            return bstack1ll1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨ࿠")
        else:
            return bstack1ll1l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪ࿡")
    elif hook_type.lower() == bstack1ll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ࿢"):
        if current_test_uuid is None:
            return bstack1ll1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪ࿣")
        else:
            return bstack1ll1l1_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡆࡃࡆࡌࠬ࿤")