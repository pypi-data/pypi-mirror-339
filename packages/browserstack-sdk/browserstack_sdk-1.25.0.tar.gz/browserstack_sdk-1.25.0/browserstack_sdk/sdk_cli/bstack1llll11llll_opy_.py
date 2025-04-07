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
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import (
    bstack1111l1ll1l_opy_,
    bstack111111111l_opy_,
    bstack11111l11ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack11l1ll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
class bstack1lll1ll11ll_opy_(bstack1lllll1l111_opy_):
    bstack1l1l1l1l111_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࠨኞ")
    bstack1l1l1ll111l_opy_ = bstack11l1l11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡦࡸࡴࠣኟ")
    bstack1l1l1lll1ll_opy_ = bstack11l1l11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡵࡰࠣአ")
    def __init__(self, bstack1llll11lll1_opy_):
        super().__init__()
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111ll11_opy_, bstack111111111l_opy_.PRE), self.bstack1l1l1ll1l11_opy_)
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.PRE), self.bstack1ll11lll11l_opy_)
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.POST), self.bstack1l1l1lll11l_opy_)
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.bstack111111l111_opy_, bstack111111111l_opy_.POST), self.bstack1l1l1l1llll_opy_)
        bstack1lll1l11ll1_opy_.bstack1ll1l11l11l_opy_((bstack1111l1ll1l_opy_.QUIT, bstack111111111l_opy_.POST), self.bstack1l1l1l111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1l11_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11l1l11_opy_ (u"ࠤࡢࡣ࡮ࡴࡩࡵࡡࡢࠦኡ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1l1ll11l1_opy_(instance, f, kwargs)
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀ࡬࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾ࠼ࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኢ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠦࠧኣ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11lll11l_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack11111l1l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1l1l111_opy_, False):
            return
        if not f.bstack1111111l11_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_):
            return
        platform_index = f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_)
        if f.bstack1ll1l11l1l1_opy_(method_name, *args) and len(args) > 1:
            bstack1l1ll1l111_opy_ = datetime.now()
            hub_url = bstack1lll1l11ll1_opy_.hub_url(driver)
            self.logger.warning(bstack11l1l11_opy_ (u"ࠧ࡮ࡵࡣࡡࡸࡶࡱࡃࠢኤ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠨࠢእ"))
            bstack1l1l1l11ll1_opy_ = args[1][bstack11l1l11_opy_ (u"ࠢࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨኦ")] if isinstance(args[1], dict) and bstack11l1l11_opy_ (u"ࠣࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢኧ") in args[1] else None
            bstack1l1l1l1ll1l_opy_ = bstack11l1l11_opy_ (u"ࠤࡤࡰࡼࡧࡹࡴࡏࡤࡸࡨ࡮ࠢከ")
            if isinstance(bstack1l1l1l11ll1_opy_, dict):
                bstack1l1ll1l111_opy_ = datetime.now()
                r = self.bstack1l1l1lll111_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡴࡨ࡫࡮ࡹࡴࡦࡴࡢ࡭ࡳ࡯ࡴࠣኩ"), datetime.now() - bstack1l1ll1l111_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack11l1l11_opy_ (u"ࠦࡸࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪ࠾ࠥࠨኪ") + str(r) + bstack11l1l11_opy_ (u"ࠧࠨካ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l1l1lll1_opy_(instance, driver, r.hub_url)
                        f.bstack1111111l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1l1l111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧኬ"), e)
    def bstack1l1l1lll11l_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1l11ll1_opy_.session_id(driver)
            if session_id:
                bstack1l1l1l11lll_opy_ = bstack11l1l11_opy_ (u"ࠢࡼࡿ࠽ࡷࡹࡧࡲࡵࠤክ").format(session_id)
                bstack1lll1llll1l_opy_.mark(bstack1l1l1l11lll_opy_)
    def bstack1l1l1l1llll_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111l1l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1ll111l_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1l11ll1_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣ࡬ࡺࡨ࡟ࡶࡴ࡯ࡁࠧኮ") + str(hub_url) + bstack11l1l11_opy_ (u"ࠤࠥኯ"))
            return
        framework_session_id = bstack1lll1l11ll1_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack11l1l11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࡂࠨኰ") + str(framework_session_id) + bstack11l1l11_opy_ (u"ࠦࠧ኱"))
            return
        if bstack1lll1l11ll1_opy_.bstack1l1l1llll1l_opy_(*args) == bstack1lll1l11ll1_opy_.bstack1l1l1l1l11l_opy_:
            bstack1l1l1l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠻ࡧࡱࡨࠧኲ").format(framework_session_id)
            bstack1l1l1l11lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠼ࡶࡸࡦࡸࡴࠣኳ").format(framework_session_id)
            bstack1lll1llll1l_opy_.end(
                label=bstack11l1l11_opy_ (u"ࠢࡴࡦ࡮࠾ࡩࡸࡩࡷࡧࡵ࠾ࡵࡵࡳࡵ࠯࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠥኴ"),
                start=bstack1l1l1l11lll_opy_,
                end=bstack1l1l1l1l1ll_opy_,
                status=True,
                failure=None
            )
            bstack1l1ll1l111_opy_ = datetime.now()
            r = self.bstack1l1l1ll1111_opy_(
                ref,
                f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠࡵࡷࡥࡷࡺࠢኵ"), datetime.now() - bstack1l1ll1l111_opy_)
            f.bstack1111111l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1ll111l_opy_, r.success)
    def bstack1l1l1l111l1_opy_(
        self,
        f: bstack1lll1l11ll1_opy_,
        driver: object,
        exec: Tuple[bstack11111l11ll_opy_, str],
        bstack1111l1ll11_opy_: Tuple[bstack1111l1ll1l_opy_, bstack111111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111l1l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1lll1ll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1l11ll1_opy_.session_id(driver)
        hub_url = bstack1lll1l11ll1_opy_.hub_url(driver)
        bstack1l1ll1l111_opy_ = datetime.now()
        r = self.bstack1l1l1ll1lll_opy_(
            ref,
            f.bstack11111l1l1l_opy_(instance, bstack1lll1l11ll1_opy_.bstack1ll1l11llll_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶࠢ኶"), datetime.now() - bstack1l1ll1l111_opy_)
        f.bstack1111111l1l_opy_(instance, bstack1lll1ll11ll_opy_.bstack1l1l1lll1ll_opy_, r.success)
    @measure(event_name=EVENTS.bstack11lll1l111_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1l1ll1ll111_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣ኷") + str(req) + bstack11l1l11_opy_ (u"ࠦࠧኸ"))
        try:
            r = self.bstack1lll11lll1l_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣኹ") + str(r.success) + bstack11l1l11_opy_ (u"ࠨࠢኺ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧኻ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤኼ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1ll11_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1l1l1lll111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡵࡩ࡬࡯ࡳࡵࡧࡵࡣ࡮ࡴࡩࡵ࠼ࠣࠦኽ") + str(req) + bstack11l1l11_opy_ (u"ࠥࠦኾ"))
        try:
            r = self.bstack1lll11lll1l_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࡹࡵࡤࡥࡨࡷࡸࡃࠢ኿") + str(r.success) + bstack11l1l11_opy_ (u"ࠧࠨዀ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦ዁") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣዂ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1lll1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1l1l1ll1111_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡴࡨ࡫࡮ࡹࡴࡦࡴࡢࡷࡹࡧࡲࡵ࠼ࠣࠦዃ") + str(req) + bstack11l1l11_opy_ (u"ࠤࠥዄ"))
        try:
            r = self.bstack1lll11lll1l_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧዅ") + str(r) + bstack11l1l11_opy_ (u"ࠦࠧ዆"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ዇") + str(e) + bstack11l1l11_opy_ (u"ࠨࠢወ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l1l1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1l1l1ll1lll_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111l1_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡶࡸࡴࡶ࠺ࠡࠤዉ") + str(req) + bstack11l1l11_opy_ (u"ࠣࠤዊ"))
        try:
            r = self.bstack1lll11lll1l_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦዋ") + str(r) + bstack11l1l11_opy_ (u"ࠥࠦዌ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤው") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨዎ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll1lll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1l1l1ll11l1_opy_(self, instance: bstack11111l11ll_opy_, f: bstack1lll1l11ll1_opy_, kwargs):
        bstack1l1l1ll1l1l_opy_ = version.parse(f.framework_version)
        bstack1l1l1ll11ll_opy_ = kwargs.get(bstack11l1l11_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡳࡳࡹࠢዏ"))
        bstack1l1l1l11l11_opy_ = kwargs.get(bstack11l1l11_opy_ (u"ࠢࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠢዐ"))
        bstack1l1lll111l1_opy_ = {}
        bstack1l1l1l111ll_opy_ = {}
        bstack1l1l1ll1ll1_opy_ = None
        bstack1l1l1l11l1l_opy_ = {}
        if bstack1l1l1l11l11_opy_ is not None or bstack1l1l1ll11ll_opy_ is not None: # check top level caps
            if bstack1l1l1l11l11_opy_ is not None:
                bstack1l1l1l11l1l_opy_[bstack11l1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨዑ")] = bstack1l1l1l11l11_opy_
            if bstack1l1l1ll11ll_opy_ is not None and callable(getattr(bstack1l1l1ll11ll_opy_, bstack11l1l11_opy_ (u"ࠤࡷࡳࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዒ"))):
                bstack1l1l1l11l1l_opy_[bstack11l1l11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࡣࡦࡹ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ዓ")] = bstack1l1l1ll11ll_opy_.to_capabilities()
        response = self.bstack1l1ll1ll111_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l1l11l1l_opy_).encode(bstack11l1l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥዔ")))
        if response is not None and response.capabilities:
            bstack1l1lll111l1_opy_ = json.loads(response.capabilities.decode(bstack11l1l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦዕ")))
            if not bstack1l1lll111l1_opy_: # empty caps bstack1l1ll1l1111_opy_ bstack1l1ll1lll11_opy_ bstack1l1ll1l111l_opy_ bstack1lll11l11l1_opy_ or error in processing
                return
            bstack1l1l1ll1ll1_opy_ = f.bstack1lllll1l1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹ࡟ࡧࡴࡲࡱࡤࡩࡡࡱࡵࠥዖ")](bstack1l1lll111l1_opy_)
        if bstack1l1l1ll11ll_opy_ is not None and bstack1l1l1ll1l1l_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭዗")):
            bstack1l1l1l111ll_opy_ = None
        if (
                not bstack1l1l1ll11ll_opy_ and not bstack1l1l1l11l11_opy_
        ) or (
                bstack1l1l1ll1l1l_opy_ < version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧዘ"))
        ):
            bstack1l1l1l111ll_opy_ = {}
            bstack1l1l1l111ll_opy_.update(bstack1l1lll111l1_opy_)
        self.logger.info(bstack11l1ll1ll_opy_)
        if os.environ.get(bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠧዙ")).lower().__eq__(bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣዚ")):
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࡤ࡫ࡸࡦࡥࡸࡸࡴࡸࠢዛ"): f.bstack1l1l1llll11_opy_,
                }
            )
        if bstack1l1l1ll1l1l_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬዜ")):
            if bstack1l1l1l11l11_opy_ is not None:
                del kwargs[bstack11l1l11_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨዝ")]
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠢࡰࡲࡷ࡭ࡴࡴࡳࠣዞ"): bstack1l1l1ll1ll1_opy_,
                    bstack11l1l11_opy_ (u"ࠣ࡭ࡨࡩࡵࡥࡡ࡭࡫ࡹࡩࠧዟ"): True,
                    bstack11l1l11_opy_ (u"ࠤࡩ࡭ࡱ࡫࡟ࡥࡧࡷࡩࡨࡺ࡯ࡳࠤዠ"): None,
                }
            )
        elif bstack1l1l1ll1l1l_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩዡ")):
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዢ"): bstack1l1l1l111ll_opy_,
                    bstack11l1l11_opy_ (u"ࠧࡵࡰࡵ࡫ࡲࡲࡸࠨዣ"): bstack1l1l1ll1ll1_opy_,
                    bstack11l1l11_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥዤ"): True,
                    bstack11l1l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢዥ"): None,
                }
            )
        elif bstack1l1l1ll1l1l_opy_ >= version.parse(bstack11l1l11_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨዦ")):
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤዧ"): bstack1l1l1l111ll_opy_,
                    bstack11l1l11_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢየ"): True,
                    bstack11l1l11_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦዩ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack11l1l11_opy_ (u"ࠧࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠧዪ"): bstack1l1l1l111ll_opy_,
                    bstack11l1l11_opy_ (u"ࠨ࡫ࡦࡧࡳࡣࡦࡲࡩࡷࡧࠥያ"): True,
                    bstack11l1l11_opy_ (u"ࠢࡧ࡫࡯ࡩࡤࡪࡥࡵࡧࡦࡸࡴࡸࠢዬ"): None,
                }
            )