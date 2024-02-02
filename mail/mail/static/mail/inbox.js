document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
  
});
  
function compose_email(reply=false,recipient='',subject,body,time) {
  remove_chaild();
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  if (reply == true){
    let subj_n = "Re: "+subject;
    let body_n = "On "+time + " " + recipient +" wrote : \n           "+body +" \n  ";
    document.querySelector('#compose-recipients').value = recipient ;
    document.querySelector('#compose-recipients').disabled = true;
    document.querySelector('#compose-subject').value = subj_n;
    document.querySelector('#compose-body').value = body_n;
    }
  else if(reply == false){
    document.querySelector('#compose-recipients').disabled = false;
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  

  const composeForm = document.querySelector("#compose-form");
  const submitHandler = (event) => {
    event.preventDefault();
    const recipients = composeForm.querySelector("#compose-recipients").value;
    const subject = composeForm.querySelector("#compose-subject").value;
    const body = composeForm.querySelector("#compose-body").value;
    fetch('/emails', {
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
        load_mailbox('sent');
    })
    .catch(error => {
        console.log("Fxailed to send email:", error);
    })
    .finally(() => {

        composeForm.removeEventListener('submit', submitHandler);
    });
  };

  composeForm.addEventListener('submit', submitHandler);
}
function remove_chaild(){
  let element = document.querySelector("#email_spe");

  if(element){
    document.body.removeChild(element);
  }
  let p_div = document.querySelector(".container");
  document.querySelectorAll(".mail_class").forEach(div =>{
    p_div.removeChild(div);
  });
}
function show_mail(id,sent = false){
  fetch('/emails/'+id)
  .then(response => response.json())
  .then(email => {
      // Print email
      document.querySelector('#emails-view').style.display = 'none';

     
            let emailView = document.createElement('div');
            emailView.style.padding = '20px';
            emailView.style.margin = '20px';
            emailView.style.border = '1px solid #ddd';
            emailView.id = "email_spe";
            emailView.style.borderRadius = '8px';
            let msg = '';
            if (email.archived){
              msg = 'Unarchive';
            }
            else{
              msg = 'Archive';
            }
       
            emailView.innerHTML = `
              <h2>${email.subject}</h2>
              <p><strong>From:</strong> ${email.sender}</p>
              <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
              <p><strong>Date:</strong> ${new Date(email.timestamp).toLocaleString()}</p>
              <hr>
              <p>${email.body}</p>
              <div style="display:flex;justify-content:space-between">
                <button id="reply-btn" style="margin-top: 20px; padding: 7px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer;">Reply</button>
                <button id="archive-btn" style="margin-top: 20px; padding: 7px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer;">${msg}</button>

              </div>
            `;
            remove_chaild();
            document.body.appendChild(emailView);
            let archive = document.querySelector("#archive-btn");
            let reply = document.querySelector("#reply-btn");
            if (sent){
              archive.style.display ='none';
              reply.style.display = "none";
            }
            reply.addEventListener('click',function(btn){
              compose_email(true,email.sender,email.subject,email.body,email.timestamp);
            });
            archive.addEventListener('click',function(){
              fetch('/emails/'+email.id, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: !email.archived
                })
              })
              load_mailbox('inbox');
            });
  });
  fetch('/emails/'+id, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
  
}
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch('/emails/'+mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      let p_div = document.querySelector(".container");

      remove_chaild();
      for (let mail of emails) {
        // Create a new div for the email
        let emailDiv = document.createElement('div');
        emailDiv.className="mail_class";
        emailDiv.style.border = "1px solid #ccc";
        emailDiv.style.padding = "10px";
        emailDiv.style.margin = "10px";
        emailDiv.value = mail.id;
        if(mailbox == 'sent'){
          emailDiv.style.backgroundColor = "#D3D3D3";
        }
        else if (mail.read){
          emailDiv.style.backgroundColor = "#B2BEB5";
        }
  
        let sender = document.createElement('h5');
        
        sender.style.fontWeight = 'bold';  
        sender.textContent = (mailbox === "inbox") ? mail.sender : mail.recipients;
        emailDiv.appendChild(sender);
    
      
        let subject = document.createElement('p');
        subject.textContent = mail.subject;
        emailDiv.appendChild(subject);
    
       
        p_div.appendChild(emailDiv);}

     
      if (mailbox == "sent"){
        document.querySelectorAll(".mail_class").forEach(di =>{di.addEventListener('click',de => {show_mail(de.currentTarget.value,true)})});

      }
      else{
        document.querySelectorAll(".mail_class").forEach(di =>{di.addEventListener('click',de => {show_mail(de.currentTarget.value)})});
      }
});


}