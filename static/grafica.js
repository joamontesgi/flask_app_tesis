function charts(){    

    // ---- CNN ----
    let benigno_cnn = parseInt(document.querySelector("#benigno_cnn").innerText);
    let DDoS_cnn = parseInt(document.querySelector("#DDoS_cnn").innerText);
    let DoSGoldenEye_cnn = parseInt(document.querySelector("#DoSGoldenEye_cnn").innerText);
    let DoSHulk_cnn = parseInt(document.querySelector("#DoSHulk_cnn").innerText);
    let DoSSlowhttptest_cnn = parseInt(document.querySelector("#DoSSlowhttptest_cnn").innerText);
    let DoSSslowloris_cnn = parseInt(document.querySelector("#DoSSslowloris_cnn").innerText);

    let ataques_cnn = [benigno_cnn, DDoS_cnn, DoSGoldenEye_cnn, DoSHulk_cnn, DoSSlowhttptest_cnn, DoSSslowloris_cnn];
    let etiquetas = ['Benigno', 'DDoS', 'DoSGoldenEye', 'DoSHulk', 'DoSSlowhttptest', 'DoSSslowloris'];

    Plotly.newPlot('barra_cnn', [{x: etiquetas, y: ataques_cnn, type: 'bar'}], {title:"CNN - Barras"});
    Plotly.newPlot('pie_cnn', [{values: ataques_cnn, labels: etiquetas, type: 'pie'}], {title:"CNN - Pie"});

    // ---- DNN ----
    let benigno_dnn = parseInt(document.querySelector("#benigno_dnn").innerText);
    let DDoS_dnn = parseInt(document.querySelector("#DDoS_dnn").innerText);
    let DoSGoldenEye_dnn = parseInt(document.querySelector("#DoSGoldenEye_dnn").innerText);
    let DoSHulk_dnn = parseInt(document.querySelector("#DoSHulk_dnn").innerText);
    let DoSSlowhttptest_dnn = parseInt(document.querySelector("#DoSSlowhttptest_dnn").innerText);
    let DoSSslowloris_dnn = parseInt(document.querySelector("#DoSSslowloris_dnn").innerText);

    let ataques_dnn = [benigno_dnn, DDoS_dnn, DoSGoldenEye_dnn, DoSHulk_dnn, DoSSlowhttptest_dnn, DoSSslowloris_dnn];

    Plotly.newPlot('barra_dnn', [{x: etiquetas, y: ataques_dnn, type: 'bar'}], {title:"DNN - Barras"});
    Plotly.newPlot('pie_dnn', [{values: ataques_dnn, labels: etiquetas, type: 'pie'}], {title:"DNN - Pie"});
}
