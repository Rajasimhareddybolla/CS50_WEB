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
  document.querySelector('#submit').addEventListener('click', (event) => {
    const to = document.querySelector("#compose-recipients").value;
    let fr = document.querySelector(".form-control").value;
    let subject = document.querySelector("#compose-subject").value;
    let content = document.querySelector("#compose-body").value; // Changed "Body" to "#compose-body"
    alert(`To: ${to}, From: ${fr}, Subject: ${subject}, Content: ${content}`); // Concatenated the values into a single string
    load_mailbox('mail');
  });
  fetch('/mails',{
    'method':'POST',
    body:JSON.stringify({

      subject:subject,
      body:content
    })
    .then(()=>response.json())
    .then(result=>{
      console.log(result)
    })

  })
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}