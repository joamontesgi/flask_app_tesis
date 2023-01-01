    function cambio(){
        let si = document.getElementById("demonSi");
        let elementos = document.getElementById("elementos");
        if(si.checked){
            elementos.innerHTML=`
            <br>
            <label for="sid">Indique el SID proporcionado desde Twilio</label>
            <input type="text" name="sid" id="sid" class="form-control" required placeholder="ACc8aa44c6c66dba22640a2ff0d5331234">
            <br>
            <label for="token">Indique el Token proporcionado desde Twilio</label>
            <input type="text" name="token" id="token" class="form-control" required placeholder="87a6524a04f87f85f7829f5b085730423781144etg566">
            <br>
            <label for="numero">Indique el número de celular al cual se enviarán las notificaciones (incluya +57)</label>
            <input type="text" name="numero_cel" id="numero" class="form-control" required placeholder="3108970106">
            <br>
            <label for="Other">Indique el número proporcionado por Twilio (incluya +)</label>
            <input type="text" name="twi" id="other" class="form-control" required placeholder="13252412729">
            <br>
            <label for="Other">Indique el mensaje en caso de que se presente un ataque</label>
            <input type="text" name="mensaje" id="other" class="form-control" required placeholder="Se ha detectado un ataque">
            <br>
            `;
        }else{
            elementos.innerHTML=`
            <label for="tiempo">Ingrese el tiempo de captura (minutos)
                <input type="number" min="1" max="60" id="tiempo" name="tiempoCaptura" class="form-control" required placeholder="Mínimo 1 - Máximo 60">
            </label>
            
            `;
        }
    }