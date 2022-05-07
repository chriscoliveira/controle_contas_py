import sqlite3


class Funcoes:
    def __init__(self, arquivo):
        self.conn = sqlite3.connect(arquivo)
        self.cursor = self.conn.cursor()

    # cria banco de dados de contas
    def criaBanco(self):
        sql = 'create table if not exists contas(id integer primary key autoincrement, conta text, valor text, parcela text, ano text, mes text, dia text, situacao text, tipo text, categoria text)'
        self.cursor.execute(sql)

    # lista contas do mes
    def listaContasMes(self, mes, ano):
        sql = 'select * from contas where mes = ? and ano = ? and categoria != "cartao" and tipo = "pagar"'
        self.cursor.execute(sql, (mes, ano))
        return self.cursor.fetchall()

    # lista contas de cartao do mes
    def listaContasMesCartao(self, mes, ano):
        sql = 'select * from contas where mes = ? and ano = ? and categoria = "cartao" and tipo = "pagar"'
        self.cursor.execute(sql, (mes, ano))
        return self.cursor.fetchall()

    # lista total de contas mes a mes
    def listaContasAno(self, ano, tipo):
        listaMes = []
        for i in range(1, 13):
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ?'
            self.cursor.execute(sql, (str(i), ano, str(tipo)))
            valor = self.cursor.fetchall()
            listaMes.append(valor[0][0])
        return listaMes

    # adiciona conta
    def cadastraConta(self, conta, valor, parcela, ano, mes, dia, situacao, tipo, categoria):
        parc = parcela
        for i in range(int(parc)):
            sql = 'insert into contas(conta, valor, parcela, ano, mes, dia, situacao, tipo, categoria) values (?,?,?,?,?,?,?,?,?)'
            if not int(mes)+i > 12:
                self.cursor.execute(sql, (conta, valor, f'{i+1}-{parcela}', ano,
                                          str(int(mes)+i), dia, situacao, tipo, categoria))
            else:
                self.cursor.execute(sql, (conta, valor, f'{i+1}-{parcela}', str(int(ano)+1),
                                          str(i-11), dia, situacao, tipo, categoria))
            self.conn.commit()

    # atualiza conta
    def atualizaConta(self, id, conta, valor, parcela, ano, mes, dia, situacao, tipo, categoria):
        sql = 'update contas set conta = ?, valor = ?, parcela = ?, ano = ?, mes = ?, dia = ?, situacao = ?, tipo = ?, categoria = ? where id = ?'
        self.cursor.execute(sql, (conta, valor, parcela, ano,
                            mes, dia, situacao, tipo, categoria, id))
        self.conn.commit()

    # deleta conta
    def deletaConta(self, id):
        sql = 'delete from contas where id = ?'
        self.cursor.execute(sql, (id,))
        self.conn.commit()

    # fecha o banco
    def fechaBanco(self):
        self.conn.close()
        print('banco fechou')

    def totalMes1(self, mes, ano, tipo, categoria=None):
        if categoria:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ? and categoria = ?'
            # colecao.cursor.execute(sql, (mes, ano, tipo, categoria))
            # total = colecao.cursor.fetchall()
        else:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ?'
            self.cursor.execute(sql, (mes, ano, tipo))
            total = self.cursor.fetchall()
        return total

    def totalMes(self, mes, ano, tipo, categoria=None, situacao=None,dia=None):
        total = None
        if categoria:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ? and categoria = ?'
            self.cursor.execute(sql, (mes, ano, tipo, categoria))
            total = self.cursor.fetchall()
        else:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ?'
            self.cursor.execute(sql, (mes, ano, tipo))
            total = self.cursor.fetchall()
        if situacao:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ? and situacao = ?'
            self.cursor.execute(sql, (mes, ano, tipo, situacao))
            total = self.cursor.fetchall()
        if dia:
            sql = 'select sum(valor) from contas where mes = ? and ano = ? and tipo = ? and dia <= ?'
            self.cursor.execute(sql, (mes, ano, tipo, dia))
            total = self.cursor.fetchall()
        return total[0][0]

    # exibe o resumo das contas do mes
    def exibeResumo(self, mes, ano):
        totalPagar = self.totalMes(mes=mes, ano=ano, tipo='pagar')
        totalReceber = self.totalMes(mes=mes, ano=ano, tipo='receber')
        totalCartao = self.totalMes(
            mes=mes, ano=ano, tipo='pagar', categoria='cartao')
        faltaPagar = self.totalMes(
            mes=mes, ano=ano, tipo='pagar', situacao='pendente')
        antesdia = self.totalMes(mes=mes, ano=ano, tipo='pagar', dia=15)
        return totalPagar, totalReceber, totalCartao, faltaPagar,antesdia


if __name__ == '__main__':
    colecao = Funcoes('contas.db')
    colecao.criaBanco()
    colecao.exibeResumo("3", "2020")
    # colecao.cadastraConta(conta='teste1', valor='50', parcela='5', ano='2020',
    #                       mes='3', dia='25', situacao='pendente', tipo='pagar', categoria='cartao')

    # colecao.atualizaConta(id=142, conta='teste2', valor='99', parcela='1-3',
    #                       ano='2022', mes='3', dia='25', situacao='pendente', tipo='pagar', categoria='casa')

    # lista = colecao.listaContasMes('3', '2020')
    # print('\nlista tudo 03-2020')
    # for conta in lista:
    #     print(conta)

    # lista1 = colecao.listaContasMesCartao('3', '2020')
    # print('\nlista cartao 03-2020')
    # for conta in lista1:
    #     print(conta)

    # totalMesaMes = colecao.listaContasAno(ano='2020', tipo='receber')
    # print('\nlista total mes a mes')
    # print(totalMesaMes)
    # # for i in totalMesaMes:
    # #     print(i)
