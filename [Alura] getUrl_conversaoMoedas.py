Import re


class ExtratorURL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url)
        self.valida_url()  # Porque que aqui não é self.url ou self.valida_url(url)?

    def sanitiza_url(self, url):
        return url.strip()

    def valida_url(self):
        if self.url == "":
            raise ValueError("A Url está vazia")
        else:
            padrão_url = re.compile(
                "(http(s)?://)?(www.)?(bytebank.com)(.br)?(/cambio)")
            match = padrão_url.match(url)
            if not match:
                raise ValueError("Url inválida")

    def get_url_base(self):
        indice_interrogação = self.url.find("?")
        url_base = self.url[:indice_interrogação]
        return url_base

    def get_url_parametros(self):
        indice_interrogação = self.url.find("?")
        url_parametro = self.url[indice_interrogação+1:]
        return url_parametro

    def get_valor_parametro(self, parametro_busca):
        indice_parametro = self.get_url_parametros().find(parametro_busca)  # 12
        # posição 12 + 5 letras + 1 = posição 24
        indice_valor = indice_parametro + len(parametro_busca) + 1
        indice_ecomercial = self.get_url_parametros().find(
            "&", indice_valor)  # vai procurar o & a partir da posição do indice valor (24)
        if indice_ecomercial == -1:  # -1 aparece quando não se encontra o que se está procurando
            valor = self.get_url_parametros()[indice_valor:]
        else:
            valor = self.get_url_parametros()[indice_valor:indice_ecomercial]
        return valor

    def __len__(self):
        return len(self.url)

    def __str__(self):
        return self.url + "\n" + "Parâmetros: " + self.get_url_parametros() + "\n" + "URL Base: " + self.get_url_base()

    def __eq__(self, other):
        return self.url == other.url


class conversaodeMoedas:
    def __init__(self, url):
        self.moeda_origem = ExtratorURL(url).get_valor_parametro("moedaOrigem")
        self.moeda_destino = ExtratorURL(
            url).get_valor_parametro("moedaDestino")
        self.quantidade = ExtratorURL(url).get_valor_parametro("quantidade")
        self.verifica_dados()
        self.converte_moedas()

    def verifica_dados(self):
        if self.moeda_origem == "" or self.moeda_destino == "" or self.quantidade == "":
            raise ValueError("Impossivel calcular, ausência de dados")

    def converte_moedas(self):
        if self.moeda_origem == "dolar":
            if self.moeda_destino == "real":
                self.valor_convertido = float(self.quantidade) * 5.10
                return self.valor_convertido, self.moeda_origem, self.moeda_destino
            else:
                raise ValueError(
                    "Só realizamos conversão do dolar para real, verifique os dados")

        if self.moeda_origem == "real":
            if self.moeda_destino == "dolar":
                self.valor_convertido = float(self.quantidade) / 5.10
                return self.valor_convertido, self.moeda_origem, self.moeda_destino
            else:
                raise ValueError(
                    "Só realizamos conversão do real para dolar, verifique os dados")

    def __str__(self):
        return "Moeda de origem:" + conversao_moedas.moeda_origem.capitalize() + "\n" + "Moeda de destino: " + conversao_moedas.moeda_destino.capitalize() + "\n" + "Valor a ser convertido: " + conversao_moedas.quantidade + "\n" + "Resultado da conversão: " + str(conversao_moedas.valor_convertido)


url = "bytebank.com/cambio?quantidade=100&moedaOrigem=real&moedaDestino=dolar"
extrator_url = ExtratorURL(url)
conversao_moedas = conversaodeMoedas(url)
print(conversao_moedas)
