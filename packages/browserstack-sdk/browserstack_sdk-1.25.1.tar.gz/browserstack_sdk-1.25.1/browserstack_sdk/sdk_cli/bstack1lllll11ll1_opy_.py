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
import json
import os
import grpc
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack1llllllllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll11ll_opy_ import bstack1lll1ll1lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1111l11ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
import os
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
class bstack1lll1ll11l1_opy_(bstack1lll1llll11_opy_):
    bstack1l1l1l11111_opy_ = bstack1ll1l1_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤ࡯࡮ࡪࡶࠥ኷")
    bstack1l1l1l1l111_opy_ = bstack1ll1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡣࡵࡸࠧኸ")
    bstack1l1l11lllll_opy_ = bstack1ll1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡲࡴࠧኹ")
    def __init__(self, bstack1lll11l111l_opy_):
        super().__init__()
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack1111l1111l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1l11lll11_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1ll11lll111_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.POST), self.bstack1l1l1l1l1l1_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.POST), self.bstack1l1l1l11lll_opy_)
        bstack1lll1ll1lll_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.QUIT, bstack1111l1l1l1_opy_.POST), self.bstack1l1l1l1111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣኺ"):
            return
        def wrapped(driver, init, *args, **kwargs):
            self.bstack1l1l11llll1_opy_(instance, f, kwargs)
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࠮ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡩ࠲ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࡀࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨኻ") + str(kwargs) + bstack1ll1l1_opy_ (u"ࠣࠤኼ"))
            threading.current_thread().bstackSessionDriver = driver
            return init(driver, *args, **kwargs)
        return wrapped
    def bstack1ll11lll111_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if f.bstack11111lllll_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l1l11111_opy_, False):
            return
        if not f.bstack11111l1l1l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_):
            return
        platform_index = f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_)
        if f.bstack1ll11llllll_opy_(method_name, *args) and len(args) > 1:
            bstack1ll11l1l1_opy_ = datetime.now()
            hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠤ࡫ࡹࡧࡥࡵࡳ࡮ࡀࠦኽ") + str(hub_url) + bstack1ll1l1_opy_ (u"ࠥࠦኾ"))
            bstack1l1l11ll11l_opy_ = args[1][bstack1ll1l1_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥ኿")] if isinstance(args[1], dict) and bstack1ll1l1_opy_ (u"ࠧࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዀ") in args[1] else None
            bstack1l1l1l111ll_opy_ = bstack1ll1l1_opy_ (u"ࠨࡡ࡭ࡹࡤࡽࡸࡓࡡࡵࡥ࡫ࠦ዁")
            if isinstance(bstack1l1l11ll11l_opy_, dict):
                bstack1ll11l1l1_opy_ = datetime.now()
                r = self.bstack1l1l1l1lll1_opy_(
                    instance.ref(),
                    platform_index,
                    f.framework_name,
                    f.framework_version,
                    hub_url
                )
                instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡪࡰ࡬ࡸࠧዂ"), datetime.now() - bstack1ll11l1l1_opy_)
                try:
                    if not r.success:
                        self.logger.info(bstack1ll1l1_opy_ (u"ࠣࡵࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧ࠻ࠢࠥዃ") + str(r) + bstack1ll1l1_opy_ (u"ࠤࠥዄ"))
                        return
                    if r.hub_url:
                        f.bstack1l1l11ll111_opy_(instance, driver, r.hub_url)
                        f.bstack1111111111_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l1l11111_opy_, True)
                except Exception as e:
                    self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤዅ"), e)
    def bstack1l1l1l1l1l1_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
            session_id = bstack1lll1ll1lll_opy_.session_id(driver)
            if session_id:
                bstack1l1l11lll1l_opy_ = bstack1ll1l1_opy_ (u"ࠦࢀࢃ࠺ࡴࡶࡤࡶࡹࠨ዆").format(session_id)
                bstack1lll111l11l_opy_.mark(bstack1l1l11lll1l_opy_)
    def bstack1l1l1l11lll_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111lllll_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l1l1l111_opy_, False):
            return
        ref = instance.ref()
        hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
        if not hub_url:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤ዇") + str(hub_url) + bstack1ll1l1_opy_ (u"ࠨࠢወ"))
            return
        framework_session_id = bstack1lll1ll1lll_opy_.session_id(driver)
        if not framework_session_id:
            self.logger.warning(bstack1ll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥ࠿ࠥዉ") + str(framework_session_id) + bstack1ll1l1_opy_ (u"ࠣࠤዊ"))
            return
        if bstack1lll1ll1lll_opy_.bstack1l1l1l1l1ll_opy_(*args) == bstack1lll1ll1lll_opy_.bstack1l1l11l1l1l_opy_:
            bstack1l1l11ll1ll_opy_ = bstack1ll1l1_opy_ (u"ࠤࡾࢁ࠿࡫࡮ࡥࠤዋ").format(framework_session_id)
            bstack1l1l11lll1l_opy_ = bstack1ll1l1_opy_ (u"ࠥࡿࢂࡀࡳࡵࡣࡵࡸࠧዌ").format(framework_session_id)
            bstack1lll111l11l_opy_.end(
                label=bstack1ll1l1_opy_ (u"ࠦࡸࡪ࡫࠻ࡦࡵ࡭ࡻ࡫ࡲ࠻ࡲࡲࡷࡹ࠳ࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡣࡷ࡭ࡴࡴࠢው"),
                start=bstack1l1l11lll1l_opy_,
                end=bstack1l1l11ll1ll_opy_,
                status=True,
                failure=None
            )
            bstack1ll11l1l1_opy_ = datetime.now()
            r = self.bstack1l1l1l11l11_opy_(
                ref,
                f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0),
                f.framework_name,
                f.framework_version,
                framework_session_id,
                hub_url,
            )
            instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡹࡴࡢࡴࡷࠦዎ"), datetime.now() - bstack1ll11l1l1_opy_)
            f.bstack1111111111_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l1l1l111_opy_, r.success)
    def bstack1l1l1l1111l_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if f.bstack11111lllll_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l11lllll_opy_, False):
            return
        ref = instance.ref()
        framework_session_id = bstack1lll1ll1lll_opy_.session_id(driver)
        hub_url = bstack1lll1ll1lll_opy_.hub_url(driver)
        bstack1ll11l1l1_opy_ = datetime.now()
        r = self.bstack1l1l1l1l11l_opy_(
            ref,
            f.bstack11111lllll_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11llll1l_opy_, 0),
            f.framework_name,
            f.framework_version,
            framework_session_id,
            hub_url,
        )
        instance.bstack11lll1l111_opy_(bstack1ll1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳࠦዏ"), datetime.now() - bstack1ll11l1l1_opy_)
        f.bstack1111111111_opy_(instance, bstack1lll1ll11l1_opy_.bstack1l1l11lllll_opy_, r.success)
    @measure(event_name=EVENTS.bstack1ll11ll1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1ll11l1l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧዐ") + str(req) + bstack1ll1l1_opy_ (u"ࠣࠤዑ"))
        try:
            r = self.bstack1llllll1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧዒ") + str(r.success) + bstack1ll1l1_opy_ (u"ࠥࠦዓ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤዔ") + str(e) + bstack1ll1l1_opy_ (u"ࠧࠨዕ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l1l11ll1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1l1l1lll1_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkInitRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡲࡦࡩ࡬ࡷࡹ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣዖ") + str(req) + bstack1ll1l1_opy_ (u"ࠢࠣ዗"))
        try:
            r = self.bstack1llllll1ll1_opy_.AutomationFrameworkInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࡶࡹࡨࡩࡥࡴࡵࡀࠦዘ") + str(r.success) + bstack1ll1l1_opy_ (u"ࠤࠥዙ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣዚ") + str(e) + bstack1ll1l1_opy_ (u"ࠦࠧዛ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11l1lll_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1l1l11l11_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkStartRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡸࡥࡨ࡫ࡶࡸࡪࡸ࡟ࡴࡶࡤࡶࡹࡀࠠࠣዜ") + str(req) + bstack1ll1l1_opy_ (u"ࠨࠢዝ"))
        try:
            r = self.bstack1llllll1ll1_opy_.AutomationFrameworkStart(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤዞ") + str(r) + bstack1ll1l1_opy_ (u"ࠣࠤዟ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢዠ") + str(e) + bstack1ll1l1_opy_ (u"ࠥࠦዡ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l1l11ll1l1_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1l1l1l11l_opy_(
        self,
        ref: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        framework_session_id: str,
        hub_url: str,
    ):
        self.bstack1ll1l11ll11_opy_()
        req = structs.AutomationFrameworkStopRequest()
        req.ref = ref
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.framework_session_id = framework_session_id
        req.hub_url = hub_url
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡳࡵࡱࡳ࠾ࠥࠨዢ") + str(req) + bstack1ll1l1_opy_ (u"ࠧࠨዣ"))
        try:
            r = self.bstack1llllll1ll1_opy_.AutomationFrameworkStop(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣዤ") + str(r) + bstack1ll1l1_opy_ (u"ࠢࠣዥ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨዦ") + str(e) + bstack1ll1l1_opy_ (u"ࠤࠥዧ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1llll1l1_opy_)
    def bstack1l1l11llll1_opy_(self, instance: bstack1llllllllll_opy_, f: bstack1lll1ll1lll_opy_, kwargs):
        bstack1l1l1l1ll1l_opy_ = version.parse(f.framework_version)
        bstack1l1l11l1ll1_opy_ = kwargs.get(bstack1ll1l1_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦየ"))
        bstack1l1l11l11ll_opy_ = kwargs.get(bstack1ll1l1_opy_ (u"ࠦࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠦዩ"))
        bstack1l1ll11lll1_opy_ = {}
        bstack1l1l1l111l1_opy_ = {}
        bstack1l1l1l1ll11_opy_ = None
        bstack1l1l1l11l1l_opy_ = {}
        if bstack1l1l11l11ll_opy_ is not None or bstack1l1l11l1ll1_opy_ is not None: # check top level caps
            if bstack1l1l11l11ll_opy_ is not None:
                bstack1l1l1l11l1l_opy_[bstack1ll1l1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬዪ")] = bstack1l1l11l11ll_opy_
            if bstack1l1l11l1ll1_opy_ is not None and callable(getattr(bstack1l1l11l1ll1_opy_, bstack1ll1l1_opy_ (u"ࠨࡴࡰࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣያ"))):
                bstack1l1l1l11l1l_opy_[bstack1ll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࡠࡣࡶࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪዬ")] = bstack1l1l11l1ll1_opy_.to_capabilities()
        response = self.bstack1l1ll11l1l1_opy_(f.platform_index, instance.ref(), json.dumps(bstack1l1l1l11l1l_opy_).encode(bstack1ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢይ")))
        if response is not None and response.capabilities:
            bstack1l1ll11lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣዮ")))
            if not bstack1l1ll11lll1_opy_: # empty caps bstack1l1ll11l11l_opy_ bstack1l1ll1l11l1_opy_ bstack1l1ll1l1111_opy_ bstack1llll11ll1l_opy_ or error in processing
                return
            bstack1l1l1l1ll11_opy_ = f.bstack1lll1ll1111_opy_[bstack1ll1l1_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡢࡳࡵࡺࡩࡰࡰࡶࡣ࡫ࡸ࡯࡮ࡡࡦࡥࡵࡹࠢዯ")](bstack1l1ll11lll1_opy_)
        if bstack1l1l11l1ll1_opy_ is not None and bstack1l1l1l1ll1l_opy_ >= version.parse(bstack1ll1l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪደ")):
            bstack1l1l1l111l1_opy_ = None
        if (
                not bstack1l1l11l1ll1_opy_ and not bstack1l1l11l11ll_opy_
        ) or (
                bstack1l1l1l1ll1l_opy_ < version.parse(bstack1ll1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫዱ"))
        ):
            bstack1l1l1l111l1_opy_ = {}
            bstack1l1l1l111l1_opy_.update(bstack1l1ll11lll1_opy_)
        self.logger.info(bstack1111l11ll_opy_)
        if os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠤዲ")).lower().__eq__(bstack1ll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧዳ")):
            kwargs.update(
                {
                    bstack1ll1l1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࡡࡨࡼࡪࡩࡵࡵࡱࡵࠦዴ"): f.bstack1l1l11l1l11_opy_,
                }
            )
        if bstack1l1l1l1ll1l_opy_ >= version.parse(bstack1ll1l1_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩድ")):
            if bstack1l1l11l11ll_opy_ is not None:
                del kwargs[bstack1ll1l1_opy_ (u"ࠥࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥዶ")]
            kwargs.update(
                {
                    bstack1ll1l1_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧዷ"): bstack1l1l1l1ll11_opy_,
                    bstack1ll1l1_opy_ (u"ࠧࡱࡥࡦࡲࡢࡥࡱ࡯ࡶࡦࠤዸ"): True,
                    bstack1ll1l1_opy_ (u"ࠨࡦࡪ࡮ࡨࡣࡩ࡫ࡴࡦࡥࡷࡳࡷࠨዹ"): None,
                }
            )
        elif bstack1l1l1l1ll1l_opy_ >= version.parse(bstack1ll1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ዺ")):
            kwargs.update(
                {
                    bstack1ll1l1_opy_ (u"ࠣࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣዻ"): bstack1l1l1l111l1_opy_,
                    bstack1ll1l1_opy_ (u"ࠤࡲࡴࡹ࡯࡯࡯ࡵࠥዼ"): bstack1l1l1l1ll11_opy_,
                    bstack1ll1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢዽ"): True,
                    bstack1ll1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦዾ"): None,
                }
            )
        elif bstack1l1l1l1ll1l_opy_ >= version.parse(bstack1ll1l1_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬዿ")):
            kwargs.update(
                {
                    bstack1ll1l1_opy_ (u"ࠨࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨጀ"): bstack1l1l1l111l1_opy_,
                    bstack1ll1l1_opy_ (u"ࠢ࡬ࡧࡨࡴࡤࡧ࡬ࡪࡸࡨࠦጁ"): True,
                    bstack1ll1l1_opy_ (u"ࠣࡨ࡬ࡰࡪࡥࡤࡦࡶࡨࡧࡹࡵࡲࠣጂ"): None,
                }
            )
        else:
            kwargs.update(
                {
                    bstack1ll1l1_opy_ (u"ࠤࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠤጃ"): bstack1l1l1l111l1_opy_,
                    bstack1ll1l1_opy_ (u"ࠥ࡯ࡪ࡫ࡰࡠࡣ࡯࡭ࡻ࡫ࠢጄ"): True,
                    bstack1ll1l1_opy_ (u"ࠦ࡫࡯࡬ࡦࡡࡧࡩࡹ࡫ࡣࡵࡱࡵࠦጅ"): None,
                }
            )