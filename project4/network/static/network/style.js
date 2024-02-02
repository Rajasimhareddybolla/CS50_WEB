
document.addEventListener('DOMContentLoaded',(event)=>{

    function edit_post(element){
        const butt = element.currentTarget;
        let span = butt.parentNode;
        const whole = span.parentNode;

        const textarea = document.createElement('textarea');
        const new_span  = document.createElement('span');
        textarea.value = span.querySelector('h5').innerText;
        textarea.style.height="50px";
        textarea.style.width = '60%';
        textarea.style.color = 'voilet';
        const button = document.createElement('button');
        button.className="edit_save_post";
        button.value = butt.value;
        button.innerHTML = "save"
        new_span.appendChild(textarea);
        new_span.appendChild(button);
        new_span.style.display = 'flex';
        new_span.style.justifyContent="space-between";
        whole.replaceChild(new_span, span);
        button.onclick = (butt)=>{edit_post_save(butt)};

    }
    function ev(e){
        const curr = e.currentTarget
        const nes = e.currentTarget.querySelector("h5");
       
        fetch('/like',{
            method:'POST',

            body :JSON.stringify({
                post_pk : curr.value,
            })
        })
        .then(response=>response.json())
        .then(result=>{
            nes.innerHTML = result.message;
        });
    }
    function edit_post_save(eve){
        let curr = eve.currentTarget;
        let mail_id = curr.value;
        let span = curr.parentElement
        let par = span.parentElement
        let edited_text = span.querySelector("textarea").value;
        const new_span = document.createElement("span");
        const h5 = document.createElement("h5");
        h5.innerHTML = edited_text;
        new_span.appendChild(h5);
        const button = document.createElement("button");
        button.value = curr.value;
        const post_pk = curr.value;
        button.innerHTML = "edited";
        button.disabled =true;
        button.style.color ="white";
        button.className ="edit_post";
        new_span.style.display ="flex";
        new_span.style.justifyContent = "space-between";
        new_span.appendChild(button);
        par.replaceChild(new_span,span);
        fetch('/edit',{
            method:'POST',
            body:JSON.stringify({
                mail_id : post_pk,
                edited_text : edited_text,
            })
        })
        .then(response=>response.json())
        .then(function(result){
            console.log(result);
        });
      
    }
        function triger(element){
            const person = element.currentTarget.value;
            fetch('/follow_trigger',{
                method:'POST',
                body:JSON.stringify({
                    id :person
                })
            })
            .then(response=>{response.json()})
            .then(result=>{
                window.location.reload(true); 
            });
        }
        document.querySelectorAll(".like_post").forEach(element => {
            element.addEventListener('click', (e)=>{ ev(e) });
        });
        document.querySelectorAll(".edit_post").forEach(element => {
            element.addEventListener('click', function(e){ edit_post(e) });
        });
        document.querySelectorAll(".profile_follow").forEach(function(button){
            button.addEventListener('click',(trig)=>triger(trig));
        })
        let ne =  document.getElementById("new");
       if(ne){
        ne.addEventListener('submit',function(event){
            const content = document.querySelector("#content");
            fetch('new',{
                method:'POST',
                body :JSON.stringify({
                    conten : content.value,
                })
            })
            .then(response=> response.json())
            .then(function(result){
                console.log(result['message']);
                content.value='';
            });
            return true;
        });
    };
});