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
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1lll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack111111l1ll_opy_ import (
    bstack11111ll1l1_opy_,
    bstack1111l1l1l1_opy_,
    bstack1llllllllll_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1llll1l1111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1111l11ll_opy_
from bstack_utils.helper import bstack1l1llll11ll_opy_
import threading
import os
import urllib.parse
class bstack1lll1ll1l11_opy_(bstack1lll1llll11_opy_):
    def __init__(self, bstack1lll1llllll_opy_):
        super().__init__()
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack1111l1111l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll11111l_opy_)
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack1111l1111l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll11l1ll_opy_)
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack11111ll11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll11l111_opy_)
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack111111l11l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.bstack1111l1111l_opy_, bstack1111l1l1l1_opy_.PRE), self.bstack1l1ll111lll_opy_)
        bstack1llll1l1111_opy_.bstack1ll1l11l1l1_opy_((bstack11111ll1l1_opy_.QUIT, bstack1111l1l1l1_opy_.PRE), self.on_close)
        self.bstack1lll1llllll_opy_ = bstack1lll1llllll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11111l_opy_(
        self,
        f: bstack1llll1l1111_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠨ࡬ࡢࡷࡱࡧ࡭ࠨቃ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡓࡧࡷࡹࡷࡴࡩ࡯ࡩࠣ࡭ࡳࠦ࡬ࡢࡷࡱࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቄ"))
            return
        def wrapped(bstack1l1ll1111ll_opy_, launch, *args, **kwargs):
            response = self.bstack1l1ll11l1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቅ"): True}).encode(bstack1ll1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቆ")))
            if response is not None and response.capabilities:
                if not bstack1l1llll11ll_opy_():
                    browser = launch(bstack1l1ll1111ll_opy_)
                    return browser
                bstack1l1ll11lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤቇ")))
                if not bstack1l1ll11lll1_opy_: # empty caps bstack1l1ll11l11l_opy_ bstack1l1ll1l11l1_opy_ bstack1l1ll1l1111_opy_ bstack1llll11ll1l_opy_ or error in processing
                    return
                bstack1l1ll11llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll11lll1_opy_))
                f.bstack1111111111_opy_(instance, bstack1llll1l1111_opy_.bstack1l1ll1l11ll_opy_, bstack1l1ll11llll_opy_)
                f.bstack1111111111_opy_(instance, bstack1llll1l1111_opy_.bstack1l1ll111l11_opy_, bstack1l1ll11lll1_opy_)
                browser = bstack1l1ll1111ll_opy_.connect(bstack1l1ll11llll_opy_)
                return browser
        return wrapped
    def bstack1l1ll11l111_opy_(
        self,
        f: bstack1llll1l1111_opy_,
        Connection: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠦࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠨቈ"):
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡩ࡯ࡳࡱࡣࡷࡧ࡭ࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ቉"))
            return
        if not bstack1l1llll11ll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack1ll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡱࡸ࠭ቊ"), {}).get(bstack1ll1l1_opy_ (u"ࠧࡣࡵࡓࡥࡷࡧ࡭ࡴࠩቋ")):
                    bstack1l1ll11ll1l_opy_ = args[0][bstack1ll1l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣቌ")][bstack1ll1l1_opy_ (u"ࠤࡥࡷࡕࡧࡲࡢ࡯ࡶࠦቍ")]
                    session_id = bstack1l1ll11ll1l_opy_.get(bstack1ll1l1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࡍࡩࠨ቎"))
                    f.bstack1111111111_opy_(instance, bstack1llll1l1111_opy_.bstack1l1ll111l1l_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡨ࡮ࡹࡰࡢࡶࡦ࡬ࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢ቏"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1ll111lll_opy_(
        self,
        f: bstack1llll1l1111_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠧࡩ࡯࡯ࡰࡨࡧࡹࠨቐ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠨࡒࡦࡶࡸࡶࡳ࡯࡮ࡨࠢ࡬ࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቑ"))
            return
        def wrapped(bstack1l1ll1111ll_opy_, connect, *args, **kwargs):
            response = self.bstack1l1ll11l1l1_opy_(f.platform_index, instance.ref(), json.dumps({bstack1ll1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቒ"): True}).encode(bstack1ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቓ")))
            if response is not None and response.capabilities:
                bstack1l1ll11lll1_opy_ = json.loads(response.capabilities.decode(bstack1ll1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቔ")))
                if not bstack1l1ll11lll1_opy_:
                    return
                bstack1l1ll11llll_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll11lll1_opy_))
                if bstack1l1ll11lll1_opy_.get(bstack1ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩቕ")):
                    browser = bstack1l1ll1111ll_opy_.bstack1l1ll1111l1_opy_(bstack1l1ll11llll_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1ll11llll_opy_
                    return connect(bstack1l1ll1111ll_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1ll11l1ll_opy_(
        self,
        f: bstack1llll1l1111_opy_,
        bstack1ll11l1l11l_opy_: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨቖ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦ቗"))
            return
        def wrapped(bstack1ll11l1l11l_opy_, bstack1l1ll111ll1_opy_, *args, **kwargs):
            contexts = bstack1ll11l1l11l_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack1ll1l1_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦቘ") in page.url:
                                    return page
                    else:
                        return bstack1l1ll111ll1_opy_(bstack1ll11l1l11l_opy_)
        return wrapped
    def bstack1l1ll11l1l1_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack1ll1l1_opy_ (u"ࠢࡳࡧࡪ࡭ࡸࡺࡥࡳࡡࡺࡩࡧࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࠽ࠤࠧ቙") + str(req) + bstack1ll1l1_opy_ (u"ࠣࠤቚ"))
        try:
            r = self.bstack1llllll1ll1_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1ll1l1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࡷࡺࡩࡣࡦࡵࡶࡁࠧቛ") + str(r.success) + bstack1ll1l1_opy_ (u"ࠥࠦቜ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቝ") + str(e) + bstack1ll1l1_opy_ (u"ࠧࠨ቞"))
            traceback.print_exc()
            raise e
    def bstack1l1ll11ll11_opy_(
        self,
        f: bstack1llll1l1111_opy_,
        Connection: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠨ࡟ࡴࡧࡱࡨࡤࡳࡥࡴࡵࡤ࡫ࡪࡥࡴࡰࡡࡶࡩࡷࡼࡥࡳࠤ቟"):
            return
        if not bstack1l1llll11ll_opy_():
            return
        def wrapped(Connection, bstack1l1ll1l111l_opy_, *args, **kwargs):
            return bstack1l1ll1l111l_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llll1l1111_opy_,
        bstack1l1ll1111ll_opy_: object,
        exec: Tuple[bstack1llllllllll_opy_, str],
        bstack1111l1l11l_opy_: Tuple[bstack11111ll1l1_opy_, bstack1111l1l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1ll1l1_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨበ"):
            return
        if not bstack1l1llll11ll_opy_():
            self.logger.debug(bstack1ll1l1_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡤ࡮ࡲࡷࡪࠦ࡭ࡦࡶ࡫ࡳࡩ࠲ࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠦቡ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped