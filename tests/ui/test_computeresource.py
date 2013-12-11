#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from tests.ui.baseui import BaseUI
from lib.ui.locators import locators


class ComputeResource(BaseUI):

    def test_create_resource(self):
        "Test to create a new libvirt Compute Resource"
        name = "KVM_123"
        url = "qemu+tcp://xxx.yyy.com:16509/system"
        self.login.login(self.katello_user, self.katello_passwd)
        self.navigator.go_to_compute_resources()
        self.compute_resource.create(name, provider_type="Libvirt", url=url)
        self.assertIsNotNone(self.compute_resource.search(name))

    def test_remove_resource(self):
        "Test to delete a Compute Resource "
        name = "KVM_123"
        url = "qemu+tcp://xxx.yyy.com:16509/system"
        self.login.login(self.katello_user, self.katello_passwd)
        self.navigator.go_to_compute_resources()
        self.compute_resource.create(name, provider_type="Libvirt", url=url)
        self.assertIsNotNone(self.compute_resource.search(name))
        self.compute_resource.delete(name, really=True)
        self.assertTrue(self.user.wait_until_element(locators["notif.success"]))  # @IgnorePep8
