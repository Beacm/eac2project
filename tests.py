from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


class MySeleniumTests(StaticLiveServerTestCase):
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creamos el superusuari isard
        user = User.objects.create_user("isard", "isard@example.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    def tearDownClass(cls):
        # para no ver los test en el navegador
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()
	    

    def test_create_user(self):
	
        # Iniciar sesión como superusuario con el usuario isard
        # Ir a la página de login del admin
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        # Verificar el título de la página
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        # Verificar que estamos en el panel de administración
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        # Crear usuario 'userstaff'
        self.selenium.get(f"{self.live_server_url}/admin/auth/user/add/")
    
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("userstaff")
        password1_input = self.selenium.find_element(By.NAME, "password1")
        password1_input.send_keys("passstaff123.")
        password2_input = self.selenium.find_element(By.NAME, "password2")
        password2_input.send_keys("passstaff123.")
        self.selenium.find_element(By.NAME, "_save").click()

        # Ir a la lista de usuarios
        self.selenium.get(f"{self.live_server_url}/admin/auth/user/")

        # Hacer clic en el usuario 'userstaff'
        self.selenium.find_element(By.XPATH, '//table//a[contains(text(), "staff")]').click()

        # Dar permisos de staff a 'userstaff'
        self.selenium.find_element(By.NAME, "is_staff").click()
        self.selenium.find_element(By.NAME, "_save").click()

        # verificamos el inicio
        # Cerrar sesión del admin isard
        self.selenium.find_element(By.ID, "logout-form").click()
        self.selenium.get(f"{self.live_server_url}/admin/login/")
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        # Intentar iniciar sesión con 'userstaff'
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys('userstaff')
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys('passstaff123.')
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
		
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")
		
    #Revisa si el elemento no existe
    def test_noSuchElement(self):
        try:
            self.selenium.find_element(By.XPATH,"//a[text()='Log out']")
            assert False, "Trobat element que NO hi ha de ser"
        except NoSuchElementException:
            pass
