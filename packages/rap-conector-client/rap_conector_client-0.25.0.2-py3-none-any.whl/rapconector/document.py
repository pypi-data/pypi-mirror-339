# -*- coding: utf-8 -*-
import warnings
from json import dumps as json_dumps

from requests_toolbelt import MultipartEncoder

from rapconector.utils import parse_or_raise


class Document:
    '''Representação de um documento no Conector.'''

    def __init__(self, client, json):
        # API client, for future requests.
        self._client = client

        #: Identificador do documento.
        self.document_id = json['documentId']

        #: Tipo do documento. Possivelmente nulo. Ver
        #: :class:`DocumentType <DocumentType>` ou
        #: :class:`ExternalDocumentType <ExternalDocumentType>`, dependendo de
        #: onde a instância foi encontrada.
        self.document_type = json.get('documentType')

        #: Identificador do grupo ao qual o documento pertence. Possivelmente
        #: nulo.
        self.group_id = json.get('groupId')

        #: Identificador do documento no contexto do cliente. Possivelmente
        #: nulo.
        self.your_number = json.get('yourNumber')

        #: Informa a origem do registro do documento.
        self.registry_origin = json.get('registryOrigin')

        #: Código de estado atual do documento. Possivelmente nulo. Ver
        #: :class:`DocumentStateCode <DocumentStateCode>`.
        self.current_state = json.get('currentState')

        #: Código de segurança do documento. Possivelmente nulo.
        self.security_code = json.get('securityCode')

        #: Recibo do documento. Possivelmente nulo.
        self.receipt = json.get('receipt')

        #: Estado de autorização do documento. Possivelmente nulo. Ver
        #: :class:`DocumentAuthorizationState <DocumentAuthorizationState>`.
        self.authorization = json.get('authorization')

        #: Outras versões desse documento. Ver
        #: :class:`VersionedDocumentData <VersionedDocumentData>`.
        self.versions = [
            VersionedDocumentInfo(version_json)
            for version_json in json.get('versions')
        ] if json.get('versions') else []

    def __repr__(self):
        return '{}(document_id={}, document_type={}, group_id={}, ' \
            'your_number={}, registry_origin={}, current_state={}, security_code={}, receipt={}, ' \
            'authorization={}, versions={})' \
            .format(self.__class__.__name__, self.document_id,
            self.document_type, self.group_id, self.your_number, self.registry_origin,
            str(self.current_state), self.security_code, self.receipt,
            self.authorization, str(self.versions))

    def update(self,
               document_type=None,
               document_data=None,
               document_file=None,
               revocation_data=None,
               update_description=None):
        '''
        Atualiza o dados de um documento, quais sejam: tipo, JSON com dados
        e/ou arquivo gerado.

        Após atualização, o documento retorna ao estado inicial reniciando sua
        geração/processamento. Documentos com estado de registro válido não são
        afetados por essa operação.

        Nos casos em que um documento já está em estado válido de registro
        (estado 10) ou suspenso, é necessário revogar todo o seu respectivo
        grupo de documentos e reiniciar o processo de registro fazendo a
        inserção de novos documentos na ordem correta.

        :param document_type: Código do tipo do documento.
        :type document_type: :class:`DocumentType <DocumentType>` ou
            :class:`ExternalDocumentType <ExternalDocumentType>`

        :param document_data: Dados do documento (string JSON).
        :type document_data: str, optional

        :param document_file: Arquivo(s) do documento, onde um arquivo é uma
            tupla ``(name (str), file (IOBase), mime_type (str))``. Opcional
            somente caso ``revocation_data`` seja informado.
        :type document_file: tuple or list(tuple), optional

        :param revocation_data: Dados para a revogação do documento. Vale notar
            que em casos de atualização dos dados de revogação do documento, o
            processamento não é reiniciado e o estado de revogação se mantém.
            Opcional somente caso ``document_file`` seja informado.
        :type revocation_data: DocumentRevocationData, optional.

        :param update_description: Mensagem de atualização.
        :type update_description: str, optional

        :return: O identificador do documento atualizado.
        :rtype: int
        '''
        fields = {}
        if document_type:
            fields['documentType'] = str(document_type)
        if document_data:
            fields['documentData'] = document_data
        if update_description:
            fields['updateDescription'] = update_description
        if document_file:
            fields['documentFile'] = document_file
        if revocation_data:
            fields['revocationData'] = revocation_data.as_json()

        encoder = MultipartEncoder(fields=fields)

        return parse_or_raise(
            self._client.session.put(
                u'{}/documents/{}'.format(self._client.base_url,
                                          self.document_id),
                data=encoder,
                headers={'Content-Type': encoder.content_type}))['documentId']

    def delete(self, cascade=False, force=False):
        '''
        Deleta este documento da base de dados do RAP Conector.

        **ATENÇÃO:** Essa operação apaga os registros apenas no Conector local,
        de forma que não deleta documentos preservados no contexto do Serviço
        RAP. Para remoção do(s) documento(s) no contexto do RAP é necessário
        revogá-lo(s) antes de ter seus dados deletados do Conector local.

        :param cascade: Se deve ocorrer remoção em cascata de documentos
            dependentes.
        :type cascade: bool, optional

        :param force: Força remoção documento no registro local ignorando o
            estado atual do mesmo no registro do Serviço RAP.
            **IMPORTANTE:** Ao utilizar o parâmetro ``force=true``, caso o
            documento já esteja presente no serviço de preservação, ele será
            automaticamente revogado antes da remoção no registro local.
        :type force: bool, optional

        :return: Número de documentos removidos.
        :rtype: int
        '''
        return parse_or_raise(
            self._client.session.delete(
                u'{}/documents/{}?cascade={}&force={}'.format(
                    self._client.base_url, self.document_id,
                    'true' if cascade else 'false',
                    'true' if force else 'false'))).get('deletedDocuments', 0)

    def get_state(self):
        '''
        Exibe o estado atual do documento.

        Em caso de erro, suspensão, re-ativação ou revogação de documento, o
        campo aditionalInfo indicará a razão de entrada em cada estado.

        As informações de suspensão, ativação e revogação podem ser utilizadas
        para mapear o histórico do documento conforme previsão na nota técnica
        referente a diplomas digitais: ver item 7.12 da Nota Técnica No.
        13/2019/DIFES/SESU/SESU.

        :rtype: DocumentState
        '''
        json = parse_or_raise(
            self._client.session.get(u'{}/documents/{}/state'.format(
                self._client.base_url, self.document_id)))

        return DocumentState(json)

    def get_history(self):
        '''
        Retorna o histórico de processamento do documento.

        :rtype: list(DocumentStateChange)
        '''
        json = parse_or_raise(
            self._client.session.get(u'{}/documents/{}/history'.format(
                self._client.base_url, self.document_id)))

        return list(map(DocumentStateChange, json))

    def get_receipt(self):
        '''
        Retorna o recibo do documento. Por exemplo::

            {
                "doc_type": "string",
                "status": "string",
                "dlt_id": "string",
                "group_id": "string",
                "client_id": "string",
                "mime_type": "string",
                "our_number": "string",
                "your_number": "string",
                "client_signature": "string",
                "data": {},
                "register_path": [],
                "created_at": "string",
                "updated_at": "string",
                "__v": int,
                "doc_hash": "string",
                "register_root": "string",
                "tx_date": "string",
                "tx_receipt": "string",
                "UUID": "string",
                "status_detail": "string",
            }

        :rtype: dict
        '''
        return parse_or_raise(
            self._client.session.get(u'{}/documents/{}/receipt'.format(
                self._client.base_url, self.document_id)))

    def download_file(self, version):
        '''
        Faz download de uma versão específica do arquivo do documento em formato
        XML.

        Caso seja indicado
        :class:`DocumentVersion.SIGNED <DocumentVersion.SIGNED>`, o serviço irá
        retornar o estado atual do documento assinado. Caso a coleta de
        assinaturas ainda não tenha sido finalizada, esse documento pode ainda
        não representar o documento final assinado. Recomenda-se seu download
        quando o documento alcançar o status registrado no serviço (estado
        :class:`DocumentStateCode.VALID <DocumentStateCode.VALID>`).

        A chamada desse método com parâmetro ``version`` contendo
        :class:`DocumentVersion.REGISTERED <DocumentVersion.REGISTERED>` faz o
        Conector realizar o download do arquivo diretamente do Serviço de
        Preservação. Esse arquivo só existe após o registro do documento no
        Serviço (estado :class:`DocumentStateCode.VALID
        <DocumentStateCode.VALID>`). O acesso ao arquivo do Serviço de
        Preservação pode ser útil nos casos em que a cópia local foi corrompida.
        Caso a instituição escolha não enviar os documentos para registro, a
        versão de registro do arquivo não existirá.

        :param version: Versão desejada do documento.
        :type version: DocumentVersion

        :return: Um objeto :class:`requests.Response <requests.Response>`, com
            a propriedade ``stream`` setada para ``True``. Para exemplos de como
            realizar o download do arquivo de forma eficiente, ver
            https://stackoverflow.com/a/39217788 e
            https://2.python-requests.org/en/master/user/quickstart/#raw-response-content.
        :rtype: :class:`requests.Response <requests.Response>`
        '''
        return parse_or_raise(self._client.session.get(
            u'{}/documents/{}/files/{}'.format(self._client.base_url,
                                               self.document_id, version),
            stream=True),
                              dont_parse=True)

    def generate_json_visualization(self):
        '''
        Gera um JSON para visualização do arquivo de um documento.

        :return: O JSON em forma de um dicionário Python.
        :rtype: dict`
        '''
        return parse_or_raise(
            self._client.session.get(
                u'{}/documents/{}/view?format=json'.format(
                    self._client.base_url, self.document_id)))

    def generate_html_visualization(self):
        '''
        Gera uma página HTML para visualização do arquivo de um documento.

        :return: Um objeto :class:`requests.Response <requests.Response>`, com
            a propriedade ``stream`` setada para ``True``. Para exemplos de como
            realizar o download do arquivo de forma eficiente, ver
            https://stackoverflow.com/a/39217788 e
            https://2.python-requests.org/en/master/user/quickstart/#raw-response-content.
        :rtype: :class:`requests.Response <requests.Response>`
        '''
        return parse_or_raise(self._client.session.get(
            u'{}/documents/{}/view?format=html'.format(self._client.base_url,
                                                       self.document_id),
            stream=True),
                              dont_parse=True)

    def suspend(self, reason):
        '''
        Suspende o documento.

        :param reason: Motivo da suspensão do documento.
        :type reason: str

        :return: Se o documento foi suspenso.
        :rtype: bool
        '''
        return bool(
            parse_or_raise(
                self._client.session.post(u'{}/documents/{}/suspend'.format(
                    self._client.base_url, self.document_id),
                                          data={'reason': reason}))['message'])

    def activate(self, reason):
        '''
        Ativa o documento.

        :param reason: Motivo da re-ativação do documento.
        :type reason: str

        :return: Se o documento foi re-ativado.
        :rtype: bool
        '''
        return bool(
            parse_or_raise(
                self._client.session.post(u'{}/documents/{}/activate'.format(
                    self._client.base_url, self.document_id),
                                          data={'reason': reason}))['message'])

    def revoke(self, reason):
        '''
        Revoga um documento no contexto do Conector e no contexto do Serviço
        RAP.

        :param reason: Motivo da revogação do documento.
        :type reason: str

        :return: Se o documento foi marcado como "irá ser revogado".
        :rtype: bool
        '''
        return bool(
            parse_or_raise(
                self._client.session.post(u'{}/documents/{}/revoke'.format(
                    self._client.base_url, self.document_id),
                                          data={'reason': reason}))['message'])

    def retry_processing(self, step=None):
        '''
        Caso o documento esteja em um estado de falha, tenta reiniciar a etapa
        desejada do processamento.

        :param step: Qual etapa para re-executar. Caso omitido, a etapa tentará
            ser inferida a partir do ``current_state`` do documento.
        :type step:
            :class:`DocumentProcessingStep <DocumentProcessingStep>`, optional

        :return: ``True`` em caso de sucesso.
        :rtype: bool
        '''
        if not step:
            cur_state = self.current_state if self.current_state is not None \
                else 0

            # If no errors, bail.
            if (DocumentStateCode.UNKNOWN < cur_state <
                    DocumentStateCode.ERROR_DURING_CREATION_PREPARATION):
                return None

            # Figure out latest step we can retry from.
            if cur_state == DocumentStateCode.UNKNOWN:
                step = 'restart-processing'
            elif cur_state < DocumentStateCode.ERROR_DURING_SIGNING_STARTING:
                step = 'retry-generation'
            elif cur_state < DocumentStateCode.ERROR_DURING_REGISTRATION:
                step = 'retry-signature'
            elif cur_state == DocumentStateCode.ERROR_DURING_REVOCATION:
                step = 'retry-revocation'
            elif cur_state == DocumentStateCode.ERROR_DURING_RESTAMPING:
                step = 'retry-restamping'
            elif cur_state >= DocumentStateCode.ERROR_DURING_REGISTRATION:
                step = 'retry-registration'
            else:
                step = 'restart-processing'

        return bool(
            parse_or_raise(
                self._client.session.post(
                    u'{}/documents/{}/{}'.format(self._client.base_url,
                                                 self.document_id,
                                                 step), ))['message'])

    def set_authorization(self, desired_auth_status, description):
        '''
        Atualiza o estado de autorização de um documento para permitir ou
        proibir a assinatura e registro de um documento após a revisão manual
        do arquivo gerado pelo Conector.

        Atenção: documentos com a revisão manual desativada terão seu estado de
        autorização atualizado para authorized automaticamente pelo Conector.

        :param desired_auth_status: Estado de autorização desejado.
        :type desired_auth_status: :class:`DocumentAuthorizationState <DocumentAuthorizationState>`

        :param description: Descrição textual para o novo estado de autorização.
        :type description: str

        :return: ``True`` em caso de sucesso.
        :rtype: bool
        '''
        parse_or_raise(
            self._client.session.patch(
                '{}/documents/{}/authorization'.format(self._client.base_url,
                                                       self.document_id),
                json={
                    "documentAuthorization": desired_auth_status,
                    "authorizationDescription": description
                }))

        return True

    def repair_timestamp(self):
        '''
        ⚠️ DEPRECIADO: Este método será removido em uma versão futura do
        Conector.

        Repara o carimbo de tempo da assinatura de arquivamento do documento
        registrado no Serviço de Preservação do RAP.

        :return: ``True`` em caso de sucesso.
        :rtype: bool
        '''
        warnings.warn(
            "Foi detectada uma chamada para o método repair_timestamp. Esse " \
            "método foi depreciado e será removido em uma versão futura do " \
            "Conector.",
            category=FutureWarning,
            stacklevel=2
        )

        parse_or_raise(
            self._client.session.post(
                '{}/documents/{}/repair-timestamp'.format(
                    self._client.base_url, self.document_id)))

        return True


class DocumentAuthenticityResult:
    '''
    Resultado da autenticação de um documento.

    Observação: o único campo que tem garantia de estar preenchido é o campo
    ``valid`` os outros campos podem ou não estar preenchidos, de acordo com a
    validade do documento.
    '''

    def __init__(self, json):
        #: Identificador da blockchain em que o documento está registrado.
        self.dlt_id = json.get('dlt_id')

        #: Código do recibo da transação de registro do documento na blockchain
        #: escolhida.
        self.tx_receipt = json.get('tx_receipt')

        #: Hash do documento registrado na blockchain.
        self.doc_hash = json.get('doc_hash')

        #: Booleano que indica se o status do documento é válido no serviço RAP.
        self.valid = json.get('valid')

        #: Raiz da estrutura de dados utilizada para registro do documento na
        #: blockchain.
        self.register_root = json.get('register_root')

        #: Identificador da instituição no serviço RAP.
        self.client_id = json.get('client_id')

        #: Identificador único do documento no serviço RAP.
        self.your_number = json.get('your_number')

        #: Data e hora de registro do documento na blockchain (timestamp Unix).
        self.register_date = json.get('register_date')

        #: Número de confirmações da transação de registro do documento na
        #: blockchain.
        self.confirmations = json.get('confirmations')

        #: Data e hora da revogação do documento na blockchain (timestamp Unix).
        self.revocation_date = json.get('revocation_date')

    def __repr__(self):
        return '{}(dlt_id={}, tx_receipt={}, doc_hash={}, valid={}, ' \
                'register_root={}, client_id={}, your_number={}, ' \
                    'register_date={}, confirmations={}, ' \
                        'revocation_date={})'.format(
            self.__class__.__name__,
            self.dlt_id,
            self.tx_receipt,
            self.doc_hash,
            self.valid,
            self.register_root,
            self.client_id,
            self.your_number,
            self.register_date,
            self.confirmations,
            self.revocation_date
        )


class DocumentFormat:
    '''Enumeração dos possíveis formatos de um documento.'''
    #: Formato JSON.
    JSON = 'json'

    #: Formato XML.
    XML = 'xml'


class DocumentGroup:
    '''Representação de um grupo de documentos.'''

    def __init__(self, json):
        #: String de identificação do grupo.
        self.group_id = json.get('groupId')

        #: Documentos pertencentes ao grupo, representados por uma lista de
        #: dicionários contendo as chaves ``document_id`` e ``document_type``.
        self.document_stubs = [{
            'document_id': x.get('documentId'),
            'document_type': x.get('documentType')
        } for x in json.get('documents')]

    def __repr__(self):
        return '{}(group_id={}, document_stubs={})'.format(
            self.__class__.__name__, self.group_id, self.document_stubs)


class DocumentGroupType:
    '''
    Enumeração dos tipos de grupos de documentos
    (ver :class:`DocumentGroup <DocumentGroup>`) existentes.
    '''
    #: Documentos Próprios. Inclui: Grupo de Diploma (2), Documentação Acadêmica
    #: (4), Histórico Escolar Integral (3) e Representações Visuais (5) e (13)
    OWN_DOCUMENTS = 1

    #: Documentos Anulados. Inclui: Grupo de Lista de Diplomas anulados (8)
    VOID_DOCUMENTS = 3

    #: Documentos de Fiscalização da Registradora. Inclui: Arquivo de Fiscalização da Registradora (9)
    REGISTRAR_AUDIT_DOCUMENTS = 4

    #: Documentos de Fiscalização da Emissora. Inclui: Grupo de Arquivo de Fiscalização da Emissora (10)
    ISSUER_AUDIT_DOCUMENTS = 5

    #: Currículos. Inclui: Grupo de Currículo Escolar (11) e Representação Visual (12)
    CURRICULUMS = 6

    #: Histórico Escolar Parcial. Inclui: Grupo de Histórico Escolar Parcial (1)
    PARTIAL_ACADEMIC_TRANSCRIPT = 7


class DocumentProcessingStep:
    '''Enumeração das possíveis etapas de processamento para re-executar.'''
    #: Para re-executar o processamento de um documento.
    PROCESSING = 'restart-processing'

    #: Para re-executar o processo de geração de um documento.
    GENERATION = 'retry-generation'

    #: Para re-executar o processo da última assinatura de um documento.
    SIGNATURE = 'retry-signature'

    #: Para re-executar o processo de todas assinaturas de um documento que
    #: ainda não esteja no estado válido, ou esteja em um estado de erro de
    #: assinatura.
    ALL_SIGNATURES = 'restart-signatures'

    #: Para re-executar o processo de revogação de um documento.
    REVOCATION = 'retry-revocation'

    #: Para re-executar o processo de registro de um documento.
    REGISTRATION = 'retry-registration'

    #: Para re-executar o processo de recarimbamento de um documento.
    RESTAMPING = 'retry-restamping'


class DocumentRegistryOrigin:
    '''Enumeração dos possíveis origens do registro de um documento.'''

    #: Registro.
    REGISTRATION = 'registration'

    #: Renotarização.
    RENOTARIZATION = 'renotarization'

    #: Atualização de assinatura.
    SIGNATURE_UPDATE = 'signature_update'


class DocumentSignature:
    '''Representação de uma assinatura em um documento.'''

    def __init__(self, json):
        #: Nome do assinante.
        self.signer = json.get('signer')

        #: Identificador do assinante.
        self.signer_id = json.get('signerId')

        #: Data e hora em que a assinatura foi coletada, em string no formato ISO 8601.
        self.signature_date = json.get('signatureDate')

        #: Data e hora de expiração da assinatura, em string no formato ISO 8601.
        self.expiration_date = json.get('expirationDate')

        #: Tag da assinatura.
        self.tag = json.get('tag')

        #: Estado da assinatura. Ver
        #: :class:`DocumentSignatureState <DocumentSignatureState>`.
        self.state = json.get('signatureState')

        #: Se a assinatura é uma assinatura de arquivamento.
        self.archiving_signature = bool(json.get('archivingSignature'))

        #: Nome do assinante substituto, caso exista.
        self.substitute_signer = json.get('substituteSigner').get('name') if \
            json.get('substituteSigner') else None

        #: Estado da assinatura substituta, caso exista. Ver
        #: :class:`DocumentSignatureState <DocumentSignatureState>`.
        self.substitute_signature_state = json \
            .get('substituteSigner').get('signatureState') if \
            json.get('substituteSigner') else None

        #: Data e hora em que a assinatura foi criada no RAP Conector, em
        #: string no formato ISO 8601.
        self.created_at = json.get('createdAt')

    def __repr__(self):
        return '{}(signer={}, signer_id={}, signature_date={}, expiration_date={}, tag={}, ' \
            'state={}, archiving_signature={}, substitute_signer={}, ' \
            'substitute_signature_state={}, created_at={})'.format(
                self.__class__.__name__, self.signer, self.signer_id,
                self.signature_date, self.expiration_date, self.tag,
                str(self.state), str(self.archiving_signature),
                self.substitute_signer, str(self.substitute_signature_state), str(self.created_at))


class DocumentSignatureState:
    '''
    Enumeração dos possíveis estados de uma
    :class:`DocumentSignature <DocumentSignature>`.
    '''
    #: Não assinado.
    NOT_SIGNED = 0

    #: Assinatura em processamento, no caso da assinatura principal.
    PROCESSING = 1

    #: Assinatura substituta concluída.
    SUBSTITUTE_PROCESSING = 1

    #: Assinatura concluída.
    SIGNED = 2


class DocumentState:
    '''Representação do estado atual do processamento de um documento.'''

    def __init__(self, json):
        #: Código de estado atual do documento. Ver
        #: :class:`DocumentStateCode <DocumentStateCode>`.
        self.current_state = json['currentState']

        #: Descrição textual do estado atual do documento.
        self.description = json['description']

        #: Informações adicionais sobre o estado atual do documento.
        self.additional_info = json['aditionalInfo']

        #: Informa a origem do registro.
        self.registry_origin = json.get('registryOrigin')

        signatures = json.get('signatures')

        #: Assinaturas do documento. Ver
        #: :class:`DocumentSignature <DocumentSignature>`. Possivelmente nulo.
        self.signatures = [DocumentSignature(s) for s in signatures] \
            if signatures else None

        #: Motivo de revogação do documento. Ver
        #: :class:`DocumentRevocationData <DocumentRevocationData>`.
        #: Possivelmente nulo.
        self.revocation = None

        revocation = json.get('revocation', {})
        if 'reason' in revocation or 'notes' in revocation:
            self.revocation = DocumentRevocationData(
                revocation.get('reason'), revocation.get('notes', ''))

        #: Data e a hora da última vez que algum dado do documento sofreu
        #: alteração, no formato ISO 8601. Possivelmente nulo.
        self.last_update = json.get('lastUpdate')

    def __repr__(self):
        return '{}(current_state={}, description={}, additional_info={}, ' \
            'registry_origin={}, signatures={}, last_update={})'.format(
            self.__class__.__name__, str(self.current_state), self.description,
            self.additional_info, self.registry_origin, str(self.signatures), self.last_update)


class DocumentStateChange:
    '''Representação do histórico de processamento de um documento.'''

    def __init__(self, json):
        #: Código de estado anterior do documento. Ver
        #: :class:`DocumentStateCode <DocumentStateCode>`.
        self.previous_state = json['previousState']

        #: Código de estado atual do documento. Ver
        #: :class:`DocumentStateCode <DocumentStateCode>`.
        self.current_state = json['currentState']

        #: Timestamp (str) referente à mudança de estado do documento.
        self.timestamp = json['timestamp']

        #: Descrição textual do estado do documento.
        self.description = json['description']

        #: Informações adicionais sobre o estado do documento.
        self.additional_info = json['aditionalInfo']

        #: Lista de transições de estado do documento. Ver
        #: :class:`DocumentStateChangeTransition <DocumentStateChangeTransition>`.
        self.update = list(
            map(DocumentStateChangeTransition, json.get('update', [])))

        # Alias (idealmente temporário!) para o atributo update. Na release
        # original que dava suporte à versão v0.25.0 do RAP Conector, o atributo
        # `update` estava errôneamente nomeado como `updates`. Para manter a
        # compatibilidade com a versão anterior, criamos esse alias.
        self.updates = self.update

    def __repr__(self):
        return '{}(previous_state={}, current_state={}, description={}, ' \
                'timestamp={}, additional_info={}, update={})'.format(
                self.__class__.__name__, str(self.previous_state),
                str(self.current_state), self.description, self.timestamp,
                self.additional_info, str(self.update))


class DocumentStateChangeTransition:
    '''Representação de uma transição de estado de um documento.'''

    def __init__(self, json):
        #: Origem do registro. Ver
        #: :class:`DocumentRegistryOrigin <DocumentRegistryOrigin>`.
        self.origin = json['origin']

        #: Descrição textual dessa transição.
        self.description = json['description']

        #: Timestamp da transição.
        self.timestamp = json['timestamp']

    def __repr__(self):
        return '{}(origin={}, description={}, timestamp={})'.format(
            self.__class__.__name__, str(self.origin), self.description,
            self.timestamp)


class DocumentStateCode:
    '''Enumeração dos possíveis estados de um :class:`Document <Document>`.'''
    # yapf: disable
    # Empty state
    UNKNOWN = 0 #: Desconhecido

    # Success states
    READY_TO_CREATE = 1 #: Pronto para gerar
    CREATED = 2 #: Gerado

    SIGNING_STARTING = 3 #: Iniciando assinatura
    SIGNING_STARTED = 4 #: Assinatura iniciada
    SIGNING_IN_PROGRESS = 5 #: Assinando documento
    SIGNED = 6 #: Documento assinado

    READY_FOR_REGISTRATION = 7 #: Pronto para registrar
    REGISTRATION_STARTED = 8 #: Registro iniciado
    REGISTRATION_FINISHED = 9 #: Processo finalizado

    VALID = 10 #: Documento válido
    SUSPENDED = 11 #: Documento suspenso

    REVOCATION_STARTED = 12 #: Iniciando revogação
    REVOCATION_IN_PROGRESS = 13 #: Revogando
    REVOKED = 14 #: Documento revogado

    # Error states
    ERROR_DURING_CREATION_PREPARATION = 500 #: Erro ao preparar a geração
    ERROR_DURING_CREATION = 501 #: Erro na geração

    ERROR_DURING_SIGNING_STARTING = 502 #: Erro ao iniciar a assinatura
    ERROR_DURING_SIGNING = 503 #: Erro ao assinar o documento

    ERROR_DURING_REGISTRATION = 504 #: Erro ao iniciar o registro
    ERROR_FINISHING_REGISTRATION = 505 #: Erro ao finalizar o registro

    ERROR_DURING_REVOCATION = 506 #: Erro na revogação

    ERROR_DURING_RESTAMPING = 507 #: Erro no recarimbamento
    # yapf: enable


class DocumentType:
    '''Enumeração dos possíveis tipos de um :class:`Document <Document>`.'''
    #: Histórico escolar parcial. Equivalente a ``partial_academic_transcript``.
    PARTIAL_ACADEMIC_TRANSCRIPT = 1

    #: Diploma digital. Equivalente a ``digital_degree``.
    DIGITAL_DEGREE = 2

    #: Histórico escolar final. Equivalente a ``final_academic_transcript``.
    FINAL_ACADEMIC_TRANSCRIPT = 3

    #: Documentação acadêmica. Equivalente a ``academic_doc_mec_degree``.
    ACADEMIC_DOC_MEC_DEGREE = 4

    #: Representação visual. Equivalente a ``visual_rep_degree``.
    VISUAL_REP_DEGREE = 5

    #: Lista de diplomas anulados. Equivalente a ``degree_revocation_list``.
    DEGREE_REVOCATION_LIST = 8

    #: Arquivo de fiscalização da IES registradora. Equivalente a ``audit_file_registry``.
    AUDIT_FILE_REGISTRAR = 9

    #: Arquivo de fiscalização da IES emissora. Equivalente a ``audit_file_issuer``.
    AUDIT_FILE_ISSUER = 10

    #: Currículo escolar digital. Equivalente a ``digital_curriculum``.
    DIGITAL_CURRICULUM = 11

    #: Representação Visual do Currículo Escolar. Equivalente a ``visual_rep_curriculum``.
    VISUAL_REP_CURRICULUM = 12

    #: Representação Visual do Histórico Escolar Integral. Equivalente a ``visual_rep_transcript``.
    VISUAL_REP_TRANSCRIPT = 13


class ExternalDocumentType:
    '''Enumeração dos possíveis tipos de um :class:`Document <Document>`.'''
    #: Diploma externo. Equivalente a ``external_degree``.
    EXTERNAL_DEGREE = 6

    #: Documentação acadêmica externa. Equivalente a ``external_academic_doc``.
    EXTERNAL_ACADEMIC_DOC = 7


class DocumentVersion:
    '''Enumeração das possíveis versões de um arquivo a ser baixado.'''
    # yapf: disable
    GENERATED = 'generatedDocument' #: Versão gerada do documento.
    SIGNED = 'signedDocument' #: Versão assinada do documento.
    REGISTERED = 'registeredDocument' #: Versão registrada do documento.
    # yapf: enable


class DocumentAuthorizationState:
    '''Enumeração dos possíveis estados de autorização de um documento.'''
    # yapf: disable
    AUTHORIZED = 'authorized' #: Autorizado.
    UNAUTHORIZED = 'unauthorized' #: Não-autorizado.
    AWAITING = 'awaiting' #: Aguardando.
    # yapf: enable


class DocumentRevocationReason:
    '''
    Enumeração das possíveis justificativas para revogação de um documento.
    '''
    #: Erro de Fato.
    ERRO_DE_FATO = "Erro de Fato"

    #: Erro de Direito.
    ERRO_DE_DIREITO = "Erro de Direito"

    #: Decisão Judicial.
    DECISAO_JUDICIAL = "Decisão Judicial"

    #: Reemissão para Complemento de Informação.
    REEMISSAO_PARA_COMPLEMENTO_DE_INFORMACAO = "Reemissão para Complemento de Informação"

    #: Reemissão para Inclusão de Habilitação.
    REEMISSAO_PARA_INCLUSAO_DE_HABILITACAO = "Reemissão para Inclusão de Habilitação"

    #: Reemissão para Anotaçao de Registro.
    REEMISSAO_PARA_ANOTACAO_DE_REGISTRO = "Reemissão para Anotaçao de Registro"


class DocumentRevocationData:
    '''Representa dados sobre a revogação de um documento.'''

    def __init__(self, reason, notes=""):
        '''
        Inicializa um objeto contendo dados sobre a revogação de um documento.

        :param reason: String contendo a justificativa da revogação.
        :type reason: DocumentRevocationReason

        :param notes: Observações adicionais sobre a revogação.
        :type notes: str, optional
        '''
        self.reason = reason
        self.notes = notes

    def as_json(self):
        '''Serializa os dados sobre a revogação, em formato JSON.'''
        return json_dumps({"reason": self.reason, "notes": self.notes})


class DocumentValidationResult:
    '''Representa os resultados da validação de um documento.'''

    def __init__(self, json):
        #: Se o documento é ou não válido.
        self.is_valid = json["valid"]

        #: Caso o documento não seja válido, é um array de strings indicando
        #: todos os erros encontrados durante a validação.
        self.errors = None

        errors = json.get("errors")
        if errors:
            self.errors = [e["message"] for e in errors]


class VersionedDocumentInfo:
    '''Representa informações básicas sobre outra versão de um documento.'''

    def __init__(self, json):
        #: Identificador dessa versão do documento.
        self.document_id = json["documentId"]

        #: Código de segurança dessa versão do documento.
        self.security_code = json["securityCode"]

        #: Código de estado dessa versão do documento. Possivelmente nulo. Ver
        #: :class:`DocumentStateCode <DocumentStateCode>`.
        self.current_state = json["currentState"]

    def __repr__(self):
        return '{}(document_id={}, security_code={}, current_state={}'.format(
            self.__class__.__name__, str(self.document_id),
            str(self.security_code), self.current_state)
