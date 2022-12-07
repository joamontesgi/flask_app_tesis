function graficas(){    
    let benigno = document.querySelector("#benigno").innerText;
    let DDoS = document.querySelector("#DDoS").innerText;
    let DoSGoldenEye = document.querySelector("#DoSGoldenEye").innerText;
    let DoSHulk = document.querySelector("#DoSHulk").innerText;
    let DoSSlowhttptest = document.querySelector("#DoSSlowhttptest").innerText;
    let DoSSslowloris = document.querySelector("#DoSSslowloris").innerText;
    
    benigno = parseInt(benigno);
    DDoS = parseInt(DDoS);
    DoSGoldenEye = parseInt(DoSGoldenEye);
    DoSHulk = parseInt(DoSHulk);
    DoSSlowhttptest = parseInt(DoSSlowhttptest);
    DoSSslowloris = parseInt(DoSSslowloris);



    var ataques = [ benigno, DDoS, DoSGoldenEye, DoSHulk, DoSSlowhttptest, DoSSslowloris]
    var etiquetas = ['Benigno', 'DDoS', 'DoSGoldenEye', 'DoSHulk', 'DoSSlowhttptest', 'DoSSslowloris']
    var data = [
        {
            x: etiquetas,
            y: ataques,
            type: 'bar',
            text: ataques.map(String),
        }
    ];
    var layout = {
        height: 500,
        width: 500, 
        title: "Comportamiento de la trama"
      };
      
    Plotly.newPlot('barra', data, layout);

    var data = [{
        values: ataques,
        labels: ['Benigno', 'DDoS', 'DoSGoldenEye', 'DoSHulk', 'DoSSlowhttptest', 'DoSSslowloris'],
        type: 'pie'
      }];
      
      var layout = {
        height: 500,
        width: 500,
        title: "Comportamiento de la trama"

      };
      
      Plotly.newPlot('pie', data, layout);
      
}
