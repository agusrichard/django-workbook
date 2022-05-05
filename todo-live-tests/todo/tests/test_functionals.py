from selenium import webdriver
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestFunctional(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.num_todos = 10
        self.xpath_username = "//label[@for='username']"
        self.xpath_password = "//label[@for='password']"

        # Using assertIn because when running tests in headless mode, the message is "Please fill out the field"
        # when running in normal mode, the message is "Please fill in the field"
        # So, we choose to use assertIn in this case
        self.required_field_message = "Please fill"

        self.assertTrue(hasattr(settings, "WEB_DRIVER_PATH"))

        options = webdriver.ChromeOptions()
        if settings.WEB_DRIVER_HEADLESS:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            executable_path=settings.WEB_DRIVER_PATH, chrome_options=options
        )
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.quit()

    def test_positive_register(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_link_text("Register").click()

        username_label = self.driver.find_element_by_xpath(self.xpath_username)
        self.assertEqual(username_label.text, "Username")

        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys("test")
        self.assertEqual(username_input.get_attribute("value"), "test")

        password_label = self.driver.find_element_by_xpath(self.xpath_password)
        self.assertEqual(password_label.text, "Password")

        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys("test")
        self.assertEqual(password_input.get_attribute("value"), "test")

        self.driver.find_element_by_id("id-submit").click()

    def test_negative_register_data_not_filled(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_link_text("Register").click()

        self.driver.find_element_by_id("id-submit").click()

        message = self.driver.find_element_by_id("id_username").get_attribute(
            "validationMessage"
        )
        self.assertIn(self.required_field_message, message)

        message = self.driver.find_element_by_id("id_password").get_attribute(
            "validationMessage"
        )
        self.assertIn(self.required_field_message, message)

    def test_negative_register_username_already_exists(self):
        self.test_positive_register()
        self.driver.find_element_by_link_text("Register").click()

        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys("test")
        self.assertEqual(username_input.get_attribute("value"), "test")

        password_label = self.driver.find_element_by_xpath(self.xpath_password)
        self.assertEqual(password_label.text, "Password")

        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys("test")
        self.assertEqual(password_input.get_attribute("value"), "test")

        self.driver.find_element_by_id("id-submit").click()

        error_msgs = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'A user with that username already exists.')]"
        )

        self.assertEqual(len(error_msgs), 1)

    def test_positive_login(self):
        self.test_positive_register()

        title = self.driver.find_elements_by_xpath("//*[contains(text(), 'Register')]")
        self.assertEqual(len(title), 1)

        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys("test")
        self.assertEqual(username_input.get_attribute("value"), "test")

        password_label = self.driver.find_element_by_xpath(self.xpath_password)
        self.assertEqual(password_label.text, "Password")

        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys("test")
        self.assertEqual(password_input.get_attribute("value"), "test")

        self.driver.find_element_by_id("id-submit").click()

    def test_negative_login_data_not_filled(self):
        self.test_positive_register()

        self.driver.find_element_by_id("id-submit").click()

        message = self.driver.find_element_by_id("id_username").get_attribute(
            "validationMessage"
        )
        self.assertIn(self.required_field_message, message)

        message = self.driver.find_element_by_id("id_password").get_attribute(
            "validationMessage"
        )
        self.assertIn(self.required_field_message, message)

    def test_negative_login_invalid_username_or_password(self):
        self.test_positive_register()

        username_input = self.driver.find_element_by_id("id_username")
        username_input.send_keys("test1")
        self.assertEqual(username_input.get_attribute("value"), "test1")

        password_label = self.driver.find_element_by_xpath(self.xpath_password)
        self.assertEqual(password_label.text, "Password")

        password_input = self.driver.find_element_by_id("id_password")
        password_input.send_keys("test1")
        self.assertEqual(password_input.get_attribute("value"), "test1")

        self.driver.find_element_by_id("id-submit").click()

        error_msgs = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Invalid username or password.')]"
        )
        self.assertEqual(len(error_msgs), 1)

        elem = self.driver.find_element_by_xpath("//button[@aria-label='Close']")
        elem.click()

    def test_positive_logout(self):
        self.test_positive_login()

        self.driver.find_element_by_link_text("Logout").click()

    def test_positive_home(self):
        self.test_positive_login()

        self.driver.find_elements_by_xpath("//*[contains(text(), 'Nothing todo...')]")

    def test_positive_create_todo(self):
        self.test_positive_login()

        self.driver.find_element_by_id("create-todo-btn").click()

        title_input = self.driver.find_element_by_id("id_title")
        title_input.send_keys("test")

        description_input = self.driver.find_element_by_id("id_description")
        description_input.send_keys("test")

        self.driver.find_element_by_id("id-submit").click()

        elems = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Nothing todo...')]"
        )
        self.assertEqual(len(elems), 0)

        todos = self.driver.find_elements_by_class_name("accordion-item")
        self.assertEqual(len(todos), 1)

    def test_positive_create_todo_total_n_todos(self):
        self.test_positive_login()

        for i in range(self.num_todos):
            self.driver.find_element_by_id("create-todo-btn").click()

            title_input = self.driver.find_element_by_id("id_title")
            title_input.send_keys(f"test-{i}")

            description_input = self.driver.find_element_by_id("id_description")
            description_input.send_keys(f"test-{i}")

            self.driver.find_element_by_id("id-submit").click()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        self.assertEqual(len(todos), self.num_todos)

    def test_positive_delete_todo(self):
        self.test_positive_create_todo_total_n_todos()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        todos[0].find_element_by_xpath("//*[contains(text(), 'Delete')]").click()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        self.assertEqual(len(todos), self.num_todos - 1)

        elems = self.driver.find_elements_by_xpath("//*[contains(text(), 'title-0')]")
        self.assertEqual(len(elems), 0)

    def test_positive_delete_all_todos(self):
        self.test_positive_create_todo_total_n_todos()

        for i in range(self.num_todos):
            todos = self.driver.find_elements_by_class_name("accordion-item")
            todos[0].find_element_by_xpath("//*[contains(text(), 'Delete')]").click()

            todos = self.driver.find_elements_by_class_name("accordion-item")
            self.assertEqual(len(todos), self.num_todos - (i + 1))

            elems = self.driver.find_elements_by_xpath(
                f"//*[contains(text(), 'title-{self.num_todos - (i + 1)}')]"
            )
            self.assertEqual(len(elems), 0)

        all_todos = self.driver.find_elements_by_class_name("accordion-item")
        self.assertEqual(len(all_todos), 0)

    def test_positive_update_todo(self):
        self.test_positive_create_todo_total_n_todos()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        todos[0].find_element_by_xpath("//*[contains(text(), 'Edit')]").click()

        title_input = self.driver.find_element_by_id("id_title")
        title_input.clear()
        title_input.send_keys("test-updated")

        description_input = self.driver.find_element_by_id("id_description")
        description_input.clear()
        description_input.send_keys("test-updated")

        self.driver.find_element_by_id("id-submit").click()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        elems = todos[0].find_elements_by_xpath("//*[contains(text(), 'test-updated')]")
        self.assertNotEqual(len(elems), 0)

    def test_positive_complete_todo(self):
        self.test_positive_create_todo_total_n_todos()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        todos[0].find_element_by_xpath("//*[contains(text(), 'Complete')]").click()

        todos = self.driver.find_elements_by_class_name("accordion-item")
        elem = todos[0].find_element_by_id("todo-status")
        self.assertEqual(elem.get_attribute("alt"), "checked")
