    function cambio(){
        let si = document.getElementById("demonSi");
        let elementos = document.getElementById("elementos");
        if(si.checked){
            elementos.innerHTML="";
        }else{
            elementos.innerHTML=`
            <label for="tiempo">Ingrese el tiempo de captura (segundos)
                <input type="number" min="10" max="3600" id="tiempo" name="tiempoCaptura" class="form-control" required>
            </label>
            
            `;
        }
    }