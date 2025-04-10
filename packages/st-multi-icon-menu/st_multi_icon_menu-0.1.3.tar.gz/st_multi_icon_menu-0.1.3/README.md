# Streamlit Multi Icon Menu Component

This custom Streamlit component allows you to easily integrate an icon menu into your Streamlit application. The component is built using [Ant Design](https://ant.design/) and provides a simple interface for creating a menu with nested items and icons. This is a fork of <https://github.com/flucas96/st_ant_menu> by Fabian Lucas. The difference is that the st_multi_icon_menu, in addition to Ant Design and FontAwasome icons, also supports the Bootstrap icon family. Bootstrap icons is also the default family in this component.

## Icon Support 

The icon prefixing convention in st_multi_icon_menu is as follows:
- Ant Design icons: Prefix with "ad-" (e.g., "ad-UserOutlined")
- FontAwesome icons: Prefix with "fa-" (e.g., "fa-ambulance")
- Bootstrap icons: Use the icon name directly (e.g., "speedometer2")

Example:
```python
menu_data = [
    {"key": "1", "label": "Ant Design Icon", "icon": "ad-UserOutlined"},
    {"key": "2", "label": "FontAwesome Icon", "icon": "fa-ambulance"},
    {"key": "3", "label": "Bootstrap Icon", "icon": "speedometer2"},
]
```

For more information on available icons from these three families, see:
- [Ant Design Icons](https://ant.design/components/icon)
- [FontAwesome Icons](https://fontawesome.com/icons)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

## Features

- Hierarchical menu structure
- Ant Design icons support
- Light and dark theme support
- Customizable CSS styling
- Multiple selection (experimental)
- Auto-adjusting menu height
- Click event handling

## Installation

To install this component, simply run:

```bash
pip install st_multi_icon_menu
```

# Usage

First, import the **st_multi_icon_menu** function from the package:
```python
from st_multi_icon_menu import st_multi_icon_menu
```

Then, create a menu data structure, and call st_multi_icon_menu with the data:

    menu_data = [
    {
        "key": "1",
        "label": "Menu Item 1",
        "icon": "UserOutlined",
    },
    {
        "key": "2",
        "label": "Menu Item 2",
        "icon": "VideoCameraOutlined",
        "disabled": True
    },
    {
        "key": "3",
        "label": "Menu Item 3",
        "icon": "UploadOutlined",
        "children": [
            {
                "key": "3-1",
                "label": "Submenu Item 1",
                "icon": "BarChartOutlined",
            },
            {
                "key": "3-2",
                "label": "Submenu Item 2",
                "icon": "CloudOutlined",
            },
        ],
    },
    ]

    selected_key = st_multi_icon_menu(menu_data)


# API

    st_multi_icon_menu(
    menu_data: List[Dict],
    key: str = "first_menu",
    defaultValue: Optional[str] = None,
    defaultSelectedKeys: Optional[str] = None,
    defaultOpenKeys: Optional[str] = None,
    additionalHeight: int = 100,
    multiple: bool = False,
    css_styling: Optional[Dict] = None,
    theme: str = "light",
    menu_click: bool = False
    ) -> Union[str, List[str]]



Parameters

menu_data (List[Dict]): The data to be displayed in the menu. Must be a list of dictionaries that conform to the Ant Design Menu item specification. See https://ant.design/components/menu/#Menu.Item for more information.

key (str, optional): The key associated with the component. This is used to ensure that the component is rendered properly when its value changes. Defaults to "first_menu".

defaultValue (Optional[str], optional): The default value to be displayed in the component. Defaults to None.

defaultSelectedKeys (Optional[str], optional): The default selected keys in the menu. Defaults to None.
defaultOpenKeys (Optional[str], optional): The default open keys in the menu. Defaults to None.
additionalHeight (int, optional): The additional height of the menu that should be added to the Streamlit iframe height. This is used to ensure that the entire menu is visible in the Streamlit app. Defaults to 100.
multiple (bool, optional): Whether the menu allows multiple selections. (Broken) Defaults to False.
css_styling (Optional[Dict], optional): A dictionary of CSS styling to be applied to the component. Defaults to None.
theme (str, optional): The theme of the menu. Can be either "light" or "dark". Defaults to "light".
menu_click (bool, optional): Set this to True to return the list of open keys on menu click, False will only return the selected key. Defaults to False.

Returns

Union[str, List[str]]: The value of the component. If menu_click is set to True, it will return a list of open keys, otherwise it will return the selected key.
