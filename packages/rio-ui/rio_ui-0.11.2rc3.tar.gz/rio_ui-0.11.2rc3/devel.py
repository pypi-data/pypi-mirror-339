import imy.inject

import rio.components.fundamental_component


import dataclasses
import io

imy.inject.clear()
import typing as t

from datetime import datetime, timezone
import inspect
import string

import fastapi
import gc
import functools
import random
import asyncio
import numpy as np
from pathlib import Path
import pandas as pd
import fastapi
import rio.docs
import plotly
import json
import rio
import rio.components.class_container
import rio.data_models
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.dev_tools_connector
import rio.app_server
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
from datetime import datetime
import rio.debug.layouter


@dataclasses.dataclass
class MyModel:
    name: str
    enabled: bool


class MyRoot(rio.Component):
    def build(self) -> rio.Component:
        form = rio.FormBuilder(
            heading="Hello, World!",
            align_x=0.5,
            align_y=0.5,
        )

        form.add_bool(
            "enabled",
            True,
        )

        return form


class RedFrame(rio.Component):
    content: rio.Component

    def build(self) -> rio.Component:
        return rio.Rectangle(
            content=rio.Container(
                self.content,
                margin=0.5,
            ),
            fill=rio.Color.RED,
        )


class MyRoot(rio.Component):
    value: float = 1.0

    def on_selection_change(
        self,
        event: rio.ListViewSelectionChangeEvent,
    ) -> None:
        print(f"Selected items: {event.selected_items}")

    def build(self) -> rio.Component:
        return RedFrame(
            rio.Button(
                "HeyHo",
            ),
            align_x=0.5,
            align_y=0.5,
        )

        items: list[str] = ["Item 1", "Item 2"]

        root_items = [
            rio.SimpleTreeItem(
                text=item,
                key=item,
                children=[rio.SimpleTreeItem(f"Sub-{item}", key=f"sub-{item}")],
            )
            for item in items
        ]

        return rio.TreeView(
            *root_items,
            selection_mode="multiple",
            on_selection_change=self.on_selection_change,
            key="dynamic_tree",
            align_x=0.5,
            align_y=0.5,
        )

        table = rio.Table(
            pd.DataFrame(
                {
                    "A": [1, 2, 3],
                    "B": [4, 5, 6],
                }
            ),
            on_press=print,
            min_width=20,
            align_x=0.5,
            align_y=0.5,
        )

        table["header", :].style(justify="right")

        table[:2, 0].style(
            justify="left",
        )

        return table


app = rio.App(
    build=MyRoot,
    default_attachments=[],
)
