// yourapp/static/js/script.js

document.addEventListener('DOMContentLoaded', function() {
  const selectAnalise = document.querySelector('select[name="nome_analise"]');
  const descricaoDiv = document.getElementById('descricao-opcao');

  const descricoes = {
    'SF_Salaries': `
        <br>
        <div align="center">
            <img src="https://storage.googleapis.com/kaggle-datasets-images/14/14/81e8c82388b48385d96cd13f645a7f2b/dataset-cover.jpeg" alt="Gráfico de Salários SF">
        </div>
        <br>
        <h3>Detalhes sobre SF Salaries</h3>
        <p>Esta análise é focada nos salários dos funcionários públicos da cidade de São Francisco.</p>
        <ul>
          <li><strong>Ano de referência:</strong> 2019</li>
          <li><strong>Fonte:</strong> <a href="https://www.kaggle.com/datasets/kaggle/sf-salaries" target="_blank">arquivo csv</a></li>
        </ul>
        <p>As informações sobre os funcionários contidas no dataset:</p>
        <ul>
            <li><strong>id:</strong> identificador único do funcionário.</li>
            <li><strong>nome:</strong> nome completo do funcionário.</li>
            <li><strong>título da função:</strong> cargo ou posição ocupada pelo funcionário.</li>
            <li><strong>salário base:</strong> remuneração mensal ou anual do funcionário sem adicionais.</li>
            <li><strong>salário de hora extra:</strong> pagamento adicional por horas trabalhadas além da carga horária regular.</li>
            <li><strong>outros pagamentos:</strong> qualquer compensação adicional recebida pelo funcionário, como bônus ou gratificações.</li>
            <li><strong>benefícios:</strong> vantagens oferecidas ao funcionário, como planos de saúde, vale-alimentação, etc.</li>
            <li><strong>pagamento total:</strong> soma do salário base, salários de horas extras e outros pagamentos.</li>
            <li><strong>pagamento total dos benefícios:</strong> valor total dos benefícios recebidos pelo funcionário.</li>
            <li><strong>ano:</strong> ano em que os dados foram coletados ou a análise foi realizada.</li>
            <li><strong>anotações:</strong> comentários ou observações adicionais relacionadas ao funcionário.</li>
            <li><strong>agências:</strong> departamentos ou agências governamentais em que os funcionários trabalham.</li>
            <li><strong>status:</strong> situação atual do funcionário, como ativo, inativo ou aposentado.</li>
        </ul>
    `,
    'Salary_Dataset_with_Extra_Features': `
      <h3> Salary_Dataset_with_Extra_Features </h3>
      <p>Descrição mais detalhada sobre a Opção 2, incluindo informações adicionais e imagens relevantes.</p>
      <img src="{% static 'images/opcao2_image.png' %}" alt="Imagem da Opção 2">
    `,
    'DataScience_salaries_2024': `
      <h3> DataScience_salaries_2024 </h3>
      <p>Informações detalhadas e contextuais sobre a Opção 3 com links e imagens complementares.</p>
      <a href="https://exemplo.com" target="_blank">Clique aqui para saber mais</a>
    `
  };

  selectAnalise.addEventListener('change', function() {
    const opcaoSelecionada = selectAnalise.value;
    descricaoDiv.innerHTML = descricoes[opcaoSelecionada] || `
      <p>Selecione um dataset acima para realizar uma nova analise de dados.</p>
      </p> <a href="https://www.kaggle.com/" target="_blank">Origem dos datasets acima</a>
    `;
  });

  // Limpa a descrição inicialmente
  descricaoDiv.innerHTML = `
    <p>Selecione um dataset acima para realizar uma nova analise de dados.</p>
    </p> <a href="https://www.kaggle.com/" target="_blank">Origem dos datasets acima</a>
  `;
});
