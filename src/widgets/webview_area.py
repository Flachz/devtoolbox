# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio, Gdk, WebKit


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/widgets/webview_area.ui")
class WebviewArea(Adw.Bin):
    __gtype_name__ = "WebviewArea"

    # Template elements
    _box = Gtk.Template.Child()
    _name_lbl = Gtk.Template.Child()
    _spinner = Gtk.Template.Child()
    _spinner_separator = Gtk.Template.Child()
    _view_btn = Gtk.Template.Child()

    _webview = WebKit.WebView()

    # Properties
    name = GObject.Property(type=str, default="")
    show_spinner = GObject.Property(type=bool, default=False)

    _blank_html = '<html><body></body></html>'

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "webarea")

        # Style and add webview
        self._webview.set_vexpand(True)
        self._webview.set_hexpand(True)
        self._webview.load_html(self._blank_html, "")
        self._webview.add_css_class("card")
        self._webview.set_property("overflow", Gtk.Overflow.HIDDEN)
        self._box.append(self._webview)

        # Property binding
        self.bind_property("name", self._name_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner, "visible", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("show-spinner", self._spinner_separator, "visible", GObject.BindingFlags.SYNC_CREATE)
        self._spinner.bind_property("visible", self._spinner_separator, "visible", GObject.BindingFlags.BIDIRECTIONAL)

        # Signals
        self._webview.connect("decide-policy", self._on_policy_decision)
        self._webview.connect("context_menu", self._disable_contex_menu)
        self._view_btn.connect("clicked", self._on_view_clicked)

    def _on_policy_decision(self, webview:WebKit.WebView, decision:WebKit.NavigationPolicyDecision, decision_type:WebKit.PolicyDecisionType):
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            uri = decision.get_navigation_action().get_request().get_uri()
            if decision.get_navigation_action().is_user_gesture() and not uri.split("#")[0] == webview.get_uri():
                decision.ignore()
                app = Gio.Application.get_default()
                window = app.get_active_window()
                Gtk.show_uri(window, uri, Gdk.CURRENT_TIME)

    def _disable_contex_menu(self, web_view:WebKit.WebView, context_menu:WebKit.ContextMenu, event:Gdk.Event, hit_test_result:WebKit.HitTestResult):
        return True

    def _on_view_clicked(self, user_data:GObject.GPointer):
        app = Gio.Application.get_default()
        window = app.get_active_window()
        Gtk.show_uri(window, self._webview.get_uri(), Gdk.CURRENT_TIME)

    def load_uri(self, uri:str):
        self._webview.load_uri(uri)
        self._view_btn.set_sensitive(True)
