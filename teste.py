def add_new_lv(self):
        conformes = 0
        nao_conformes = 0
        nao_aplicaveis = 0
        
        connection = pymysql.connect(host='database-1.cb5zjpyynl3k.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='pawaresoftwares',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



        today = str(date.today())

        self.store = JsonStore("userProfile.json")
        nome = self.store.get('UserInfo')['name']
        email = self.store.get('UserInfo')['email']

        results = []

        for i in range(1,9):
            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_c.active == True:
                results.append('Conforme')
                conformes += 1



            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_nc.active == True:
                results.append('Não conforme')
                nao_conformes += 1


            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_na.active == True:
                results.append('Não aplicável')
                nao_aplicaveis += 1

        porcentagem_conformes = conformes * 100 / 9

        status_lv = ''

        if porcentagem_conformes < 100:
            status_lv = 'Pendente'

        else:
            status_lv = 'Concluído'

        lv={}

        for i in range(1,9):

            lv = {
                "nome_lv": self.strng.get_screen('checklistName').ids.name_text_field_lv.text,
                "descricao_lv": self.strng.get_screen('checklistName').ids.descricao_text_field_lv.text,
                "nome_usuario": nome,
                "email_usuario": email,
                "Data_emissao": today.replace('-', '/'),
                "porcentagem_c": round(porcentagem_conformes, 2),
                "quantidade_nc": nao_conformes,
                "quantidade_na": nao_aplicaveis,
                "lv_status": status_lv,

                "item1_nome": "Os locais adjacentes das caixas estão limpos e organizados?",
                "item1_resultado": results[i - 1],
                "item1_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item1_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item1_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item2_nome": "As caixas estão com acúmulo excessivo de gordura?",
                "item2_resultado": results[i - 1],
                "item2_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item2_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item2_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item3_nome": "As caixas de gordura estão obstruídas?",
                "item3_resultado": results[i - 1],
                "item3_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item3_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item3_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item4_nome": "Há evidências de transbordo?",
                "item4_resultado": results[i - 1],
                "item4_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item4_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item4_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item5_nome": "Há evidência de odores?",
                "item5_resultado": results[i - 1],
                "item5_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item5_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item5_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item6_nome": "Há detritos de alimentos, sobras de embalagens, entre outros?",
                "item6_resultado": results[i - 1],
                "item6_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item6_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item6_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item7_nome": "Há telas (grade) de retenção nas áreas internas do refeitório cin objetivo de reter sobras de alimentos?",
                "item7_resultado": results[i - 1],
                "item7_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item7_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item7_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item8_nome": "As tampas das caixas estão encaixadas de acordo com a construção?",
                "item8_resultado": results[i - 1],
                "item8_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item8_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item8_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

                "item9_nome": "O efluente está sendo direcionado para a Estação de tratamento de Efluente - ETE?",
                "item9_resultado": results[i - 1],
                "item9_acao": self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text,
                "item9_prazo": self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text,
                "item9_responsavel": self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text,

            }

        for data in lv:
            print(data)