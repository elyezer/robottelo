"""Unit tests for the ``subscription`` paths.

A full API reference for subscriptions can be found here:
https://<sat6.com>/apidoc/v2/subscriptions.html

"""
from nailgun import entities
from nailgun.entity_mixins import TaskFailedError
from robottelo.common import manifests
from robottelo.test import APITestCase


class SubscriptionsTestCase(APITestCase):
    """Tests for the ``subscriptions`` path."""

    def test_positive_create_1(self):
        """@Test: Upload a manifest.

        @Assert: Manifest is uploaded successfully

        @Feature: Subscriptions

        """
        org = entities.Organization().create()
        with open(manifests.clone()) as handle:
            entities.Subscription().upload({'organization_id': org.id}, handle)

    def test_positive_delete_1(self):
        """@Test: Delete an Uploaded manifest.

        @Assert: Manifest is Deleted successfully

        @Feature: Subscriptions

        """
        cloned_manifest_path = manifests.clone()
        org = entities.Organization().create()
        sub = entities.Subscription()
        payload = {'organization_id': org.id}
        with open(cloned_manifest_path) as handle:
            sub.upload(payload, handle)
        self.assertGreater(len(sub.subscriptions(payload)), 0)
        sub.delete_manifest(payload)
        self.assertEqual(len(sub.subscriptions(payload)), 0)

    def test_negative_create_1(self):
        """@Test: Upload the same manifest to two organizations.

        @Assert: The manifest is not uploaded to the second organization.

        @Feature: Subscriptions

        """
        manifest_path = manifests.clone()
        sub = entities.Subscription()
        orgs = [entities.Organization().create() for _ in range(2)]
        with open(manifest_path) as handle:
            sub.upload({'organization_id': orgs[0].id}, handle)
        payload = {'organization_id': orgs[1].id}
        with self.assertRaises(TaskFailedError):
            with open(manifest_path) as handle:
                sub.upload(payload, handle)
        self.assertEqual(len(sub.subscriptions(payload).subscriptions()), 0)
