from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import Select

MAX_WAIT = 10

class NewVsitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome()

	def tearDown(self):
		self.browser.quit()

	# Auxiliary method 
	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except(AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_layout_and_styling(self):
        # Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
	
		# She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

	def test_priority(self):
		
		# Edith ouviu falar que agora a aplicação online de lista de tarefas

		# aceita definir prioridades nas tarefas do tipo baixa, média e alta

		# Ela decide verificar a homepage

		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# Ela percebe que o título da página e o cabeçalho mencionam

		# listas de tarefas com prioridade (priority to-do)

		self.assertIn('priority To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('priority To-Do', header_text)

		# Ela é convidada a inserir um item de tarefa e a prioridade da 

		# mesma imediatamente

		header_text = self.browser.find_element_by_tag_name('h3').text
		self.assertIn('Please, insert an item and the priority', header_text)

		# Ela digita "Comprar anzol" em uma nova caixa de texto

		# e assinala prioridade alta no campo de seleção de prioridades

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		inputbox.send_keys('Comprar anzol')
		
		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('alta')

		inputbox.send_keys(Keys.ENTER)

		# Quando ela tecla enter, a página é atualizada, e agora

		# a página lista "1 - Comprar anzol - prioridade alta"

		# como um item em uma lista de tarefas

		self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')

		# Ainda continua havendo uma caixa de texto convidando-a a 

		# acrescentar outro item. Ela insere "Comprar cola instantânea"

		# e assinala prioridade baixa pois ela ainda tem cola suficiente

		# por algum tempo

		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('baixa')

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		inputbox.send_keys('Comprar cola instantânea')

		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_list_table('2 - Comprar cola instantânea - prioridade baixa')

		# Edith se pergunta se o site lembrará de sua lista. Então
		# ela nota que o site gerou um URL único para ela -- há um 
		# pequeno texto explicativo para isso.

		header_text = self.browser.find_element_by_tag_name('h4').text
		self.assertIn('Please, save this url to visit your priority list', header_text)

		#------------------------------

		# Ela acessa essa URL -- sua lista de tarefas continua lá.

		# Edith inicia uma nova lista de tarefas
		self.browser.get(self.browser.current_url)
		self.browser.set_window_size(1024, 768)

		#Ela percebe que sua lista te um URL único
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		self.wait_for_row_in_list_table('1 - Comprar anzol - prioridade alta')
		self.wait_for_row_in_list_table('2 - Comprar cola instantânea - prioridade baixa')

		self.browser.quit()

	def test_can_start_a_list_for_one_user(self):
		# Edith ouviu falar de uma nova aplicação online interessante
		# para lista de tarefas. Ela decide verificar a homepage

		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# Ela percebe que o título da página e o cabeçalho mencionam
		# listas de tarefas (to-do)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# Ela é convidada a inserir um item de tarefa imediatamente

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# Ela digita "Buy peacock feathers" (Comprar penas de pavão)
		# em uma nova caixa de texto (o hobby de Edith é fazer iscas
		# para pesca com fly)

		inputbox.send_keys('Buy peacock feathers')

		# Quando ela tecla enter, a página é atualizada, e agora
		# a página lista "1 - Buy peacock feathers" como um item em 
		# uma lista de tarefas

		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('baixa')

		inputbox.send_keys(Keys.ENTER)

		# Ainda continua havendo uma caixa de texto convidando-a a 
		# acrescentar outro item. Ela insere "Use peacock feathers 
		# to make a fly" (Usar penas de pavão para fazer um fly - 
		# Edith é bem metódica)

		inputbox = self.browser.find_element_by_id('id_new_item')

		inputbox.send_keys("Use peacock feathers to make a fly")

		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('baixa')

		inputbox.send_keys(Keys.ENTER)

		# A página é atualizada novamente e agora mostra os dois
		# itens em sua lista
		self.wait_for_row_in_list_table('1 - Buy peacock feathers - prioridade baixa')
		self.wait_for_row_in_list_table('2 - Use peacock feathers to make a fly - prioridade baixa')

		# Satisfeita, ela volta a dormir

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Edith inicia uma nova lista de tarefas
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		inputbox = self.browser.find_element_by_id('id_new_item')
		
		inputbox.send_keys('Buy peacock feathers')

		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('baixa')

		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 - Buy peacock feathers - prioridade baixa')

		#Ela percebe que sua lista te um URL único
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#Agora um novo usuário, Francis, chega ao site

		## Usamos uma nova versão do navegador para garantir que nenhuma 
		## informação de Edith está vindo de cookies, etc
		
		self.browser.quit()
		
		#--------------------------------------------------

		self.browser = webdriver.Chrome()

		# Francis acessa a página inicial. Não há sinal da lista de Edith
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)
		
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis inicia uma nova lista inserindo um novo item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		
		inputbox.send_keys('Buy milk')

		select = Select(self.browser.find_element_by_id('item_new_priority'))

		select.select_by_value('baixa')

		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1 - Buy milk - prioridade baixa')

		# Francis obtém seu próprio URL exclusivo
		francis_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.assertNotEqual( francis_list_url, edith_list_url)

		# Novamente não há sinal algum da lista de Edith
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		self.browser.quit()

		# Fim