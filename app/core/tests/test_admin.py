"""
Tests for the Django admin modifications.
"""


from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    """
        testの準備を行うためにsetUpメソッドを使用.
        setUpメソッドは、各テストメソッドが実行される前に実行されるコードを定義.
        これにより、テストの前提条件を設定したり、共通のテストデータを準備したりできる.

        ps: クラス全体の準備や後片付けが必要な場合は、setUpClassとtearDownClassメソッドを使い.
        これらのメソッドはクラス全体に対して一度だけ呼び出される.
    """
    def setUp(self):

        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
