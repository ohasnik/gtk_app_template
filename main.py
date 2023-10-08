import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='GTK app template')
        self.set_default_size(width=800, height=600)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(content=vbox)

        header_bar = Gtk.HeaderBar.new()
        vbox.append(child=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )
        menu_button_model.append('About', 'app.about')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        label = Gtk.Label.new()
        label.set_label(str='Click on the menu and select on')
        label.set_vexpand(expand=True)
        vbox.append(child=label)


class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='com.ondhassoftware.template.gtk',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Action `app.preferences` was active.')

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow.new()
        dialog.set_transient_for(parent=self.get_active_window())
        dialog.set_application_name('GTK app template')
        dialog.set_version('2023.10.08')
        dialog.set_developer_name('ondhas SOFTWARE')
        dialog.set_license_type(Gtk.License(Gtk.License.CUSTOM))
        dialog.set_comments('GTK app template')
        dialog.set_website('https://ondhassoftware.com')
        dialog.set_issue_url("https://github.com/ondhas")
        dialog.set_support_url("https://support.ondhassoftware.com")
        dialog.add_credit_section('Contributors', ['Ondřej Hasník'])
        dialog.set_translator_credits('Ondřej Hasník https://github.com/ondhas')
        dialog.set_documenters(['Ondřej Hasník https://github.com/ondhas'])
        dialog.set_designers(['Ondřej Hasník https://github.com/ondhas'])
        dialog.set_artists(['Ondřej Hasník https://github.com/ondhas'])
        dialog.set_copyright('© 2023 ondhas SOFTWARE')
        dialog.set_developers(['Ondřej Hasník https://github.com/ondhas'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.set_release_notes('Notes for version')
        dialog.set_debug_info('Debug info')
        dialog.present()

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'app.{name}',
                accels=shortcuts,
            )


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)