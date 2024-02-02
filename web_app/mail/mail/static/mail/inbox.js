document.addEventListener('DOMContentLoaded', function() {
  
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Add event listener to prevent form submission
  const composeForm = document.querySelector("#compose-form");
  const submitHandler = (event) => {
    event.preventDefault();
    const recipients = composeForm.querySelector("#compose-recipients").value;
    const subject = composeForm.querySelector("#compose-subject").value;
    const body = composeForm.querySelector("#compose-body").value;
    fetch('/email s', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('Sent');
    })
    .catch(error => {
        console.log("Failed to send email:", error);
    })
    .finally(() => {
        // Remove the submit event listener
        composeForm.removeEventListener('submit', submitHandler);
    });
  };}
function mail_listing(mail_id) {

  fetch('/emails/' + mail_id)
    .then(response => response.json())
    .then(result => {
      const breakd = document.createElement("br");
      console.log(result.id);
      document.querySelector('#emails-view').style.display = 'none';
      const body = document.querySelector("body");

      let div = document.createElement('div');
      div.id = "temp";
      div.style.border = "1px solid #ccc";
      div.style.padding = "10px";
      div.style.margin = "10px";
      div.style.backgroundColor = "#f9f9f9";

      let h = document.createElement('h6');
      h.style.display = "inline";
      const div_1 = document.createElement("div");
      h.innerHTML = "From: ";
      div_1.appendChild(h);
      const from = document.createTextNode(result.sender);
      div_1.appendChild(from);
      div.append(div_1);
      h = document.createElement('h6');
      const div_2 = document.createElement("div");
      h.style.display = "inline";
      h.innerHTML = 'To: ';
      div_2.appendChild(h);
      const to = document.createTextNode(result.recipients);
      div_2.appendChild(to);
      div.appendChild(div_2);
      let div_3 = document.createElement("div");
      h = document.createElement('h6');
      h.style.display = "inline";
      h.innerHTML = 'Subject: ';
      div_3.appendChild(h);
      const subject = document.createTextNode(result.subject);
      div_3.appendChild(subject);
      div.appendChild(div_3);
      h = document.createElement('h6');
      h.style.display = "inline";
      h.innerHTML = 'TimeStamp: ';
      div.appendChild(h);
      const time = document.createTextNode(h.value + mail.timestamp);
      div.appendChild(time);
      div.appendChild(breakd);

      const br = document.createElement("hr");
      div.appendChild(br);

      const content = document.createTextNode(mail.body);
      div.appendChild(content);
      const archive = document.createElement("button");
      archive.style.backgroundColor = "blue";
      archive.style.color = "white";
      archive.style.border = "none";
      archive.style.padding = "10px";
      archive.style.marginRight = "5px";
      archive.style.borderRadius= "15px";

      const reply = document.createElement("button");
      reply.style.backgroundColor = "green";
      reply.style.color = "white";
      reply.style.border = "none";
      reply.style.padding = "10px";
      reply.style.marginRight = "5px";
      reply.style.borderRadius= "10px";

      reply.innerText = "Reply";
      archive.innerText = "archive";
      if (mail.archived){
        archive.innerText = "Unarchive";
      }
      div.append(br);
      div.append(reply);
      reply.addEventListener("click",()=>{
        compose_email(mail);
      });
      archive.addEventListener('click',()=>{
        archive_mail(mail.id,mail.archived);
      });
      div.appendChild(archive);
      body.appendChild(div);

    });

} // Added closing parenthesis

function archive_mail(mail_id, state){
  fetch('/emails/'+mail_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !state,
        read :true,
    })
  });
  load_mailbox("inbox");
} // Added closing parenthesis

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  try{
    let collec = document.querySelectorAll('#temp');
    collec.forEach(elem =>{elem.style.display="none";})
  }
  catch (e ){
    console.log(e);
  }
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  let url = "/emails/"+mailbox
  const collections = []
  const p_div = document.getElementById("emails-view");
  fetch(url)
  .then(response=>response.json())
  .then(result=>{
    for (mail of result){
      let div = document.createElement('div');
      let name_d;
      name_d =document.createElement("h5");
 
      if (mailbox == "inbox"){
        name_d.innerHTML = mail.sender;
      }
      else if (mailbox == "sent"){
         name_d.innerHTML=  mail.recipients;
      }

      div.style.border = "1px solid #ccc";
      div.style.padding = "10px";
      div.style.margin = "10px";
      
      const div_1_new = document.createElement("div");
      const div_2_new = document.createElement("div");
      const subject_d_new = document.createTextNode(mail.subject);
      const time_d_new = document.createTextNode(mail.timestamp);
      div_1_new.appendChild(name_d);
      div_1_new.appendChild(subject_d_new);
      div_2_new.appendChild(time_d_new);
      div.appendChild(div_1_new);
      div.appendChild(div_2_new);
      div.style.display = "flex";
      div.style.justifyContent = "space-between";
      div.style.flexWrap = "wrap";
      div.style.alignItems = "center";
      p_div.appendChild(div);
      collections.push(div);

      div.addEventListener('click', () => {
        console.log(mail.id);
        mail_listing(mail.id);
      });

      if (mail.read) {
        div.style.backgroundColor = "#f9f9f9";
      } else {
        div.style.backgroundColor = "yellow";
      }
    }
  });
  

}