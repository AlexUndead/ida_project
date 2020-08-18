import os
from selenium import webdriver
from django.test import LiveServerTestCase
from django.conf import settings

TEST_IMAGE_PATH = "/functional_tests/image/"
TEST_IMAGE_NAME = "2e2d97e2ce9059a06b285c5d7293d1a8a63ee836.jpg"


class ImageLoaderTest(LiveServerTestCase):
    """тест модуля загрузки изображений"""
    def setUp(self) -> None:
        '''установка'''
        self.browser = webdriver.Chrome('/var/www/html/Projects/selenium-drivers/chrome/80/chromedriver')

    def tearDown(self) -> None:
        '''демонтаж'''
        os.remove(str(settings.BASE_DIR) + '/media/image/' + TEST_IMAGE_NAME)
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
        upload_image_file_input.send_keys(str(settings.BASE_DIR) + TEST_IMAGE_PATH + TEST_IMAGE_NAME)
        self.browser.find_element_by_id('upload_image_form_submit').click()

        # После успешного сохранения, пользователь попал на страницу
        # изменения размеров изображения. Так же на этой странице есть
        # ранее загруженное изображение        
        self.browser.find_element_by_id('change_size_image_form')
        uploaded_image = self.browser.find_element_by_id('uploaded_image')
        self.assertIn(TEST_IMAGE_NAME, uploaded_image.get_attribute('src'))

        # Теперь пользователь решил изменить ширину изображения
        self.browser.find_element_by_id('change_width_image_input').send_keys('400')
        self.browser.find_element_by_id('change_resize_form_submit').click()

        # Страница перезагрузилась и теперь у изображения ранее
        # введенные размеры
        uploaded_image = self.browser.find_element_by_id('uploaded_image')
        self.assertEqual(uploaded_image.size['weight'], 400)
        self.assertEqual(uploaded_image.size['height'], 400)
