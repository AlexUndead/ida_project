import os
from selenium import webdriver
from django.test import LiveServerTestCase

TEST_IMAGE_PATH = "/functional_tests/image/noavatar.jpg"


class ImageLoaderTest(LiveServerTestCase):
    """тест модуля загрузки изображений"""
    def setUp(self) -> None:
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self) -> None:
        '''демонтаж'''
        self.browser.quit()

    def test_loader_image(self) -> None:
        """тест загрузки изображения"""
        # Пользователь зашел на главную страницу
        self.browser.get(self.live_server_url)

        # Он убедился что его список загруженных изображений пуст
        upload_image_list = self.browser.find_element_by_id('uploaded_image_list')
        self.assertEqual(upload_image_list.text, 'Нет доступных изображений')

        # Пользователь решил добавить изображений 
        # и перешел на страницу с формой загрузки изображений
        self.browser.find_element_by_id('upload_image_link').click()

        # Добавил изображение и попытался сохранить его 
        upload_image_file_input = self.browser.find_element_by_id('upload_image_file_input')
        upload_image_file_input.send_keys(os.getcwd() + TEST_IMAGE_PATH)
        self.browser.find_element_by_id('upload_image_form_submit').click()

        # После успешного сохранения, пользователь попал на страницу
        # изменения размеров изображения. Так же на этой странице есть
        # ранее загруженное изображение
        change_size_image_form = self.browser.find_element_by_id('change_size_image_from')
