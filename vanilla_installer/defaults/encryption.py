# disk.py
#
# Copyright 2022 mirkobrombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundationat version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gio, GLib, GObject, Adw


@Gtk.Template(resource_path="/org/vanillaos/Installer/gtk/default-encryption.ui")
class VanillaDefaultEncryption(Adw.Bin):
    __gtype_name__ = "VanillaDefaultEncryption"

    btn_next = Gtk.Template.Child()
    use_encryption_switch = Gtk.Template.Child()
    password_entry = Gtk.Template.Child()
    confirm_password_entry = Gtk.Template.Child()

    valid_passwords = False

    def __init__(self, window, distro_info, key, step, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__distro_info = distro_info
        self.__key = key
        self.__step = step

        self.use_encryption_switch.connect("state-set", self.__on_encryption_switch_toggled)
        self.btn_next.connect("clicked", self.__on_btn_next_clicked)
        self.password_entry.connect('changed', self.__on_password_changed)
        self.confirm_password_entry.connect('changed', self.__on_password_changed)

        self.__verify_continue()

    def __on_btn_next_clicked(self, button):
        self.__window.next()

    def __on_encryption_switch_toggled(self, widget, state):
        if widget.get_active():
            self.__on_password_changed()
        else:
            self.__verify_continue()

    def __on_password_changed(self, *args):
        password = self.password_entry.get_text().strip()
        confirm_password = self.confirm_password_entry.get_text().strip()

        if password == "" and confirm_password == "":
            self.valid_passwords = False;
        elif password == confirm_password:
            self.valid_passwords = True;
            self.confirm_password_entry.remove_css_class('error')
        else:
            self.valid_passwords = False;
            self.confirm_password_entry.add_css_class('error')

        self.__verify_continue();

    def __verify_continue(self):
        self.btn_next.set_sensitive(not self.use_encryption_switch.get_active() or self.valid_passwords)
