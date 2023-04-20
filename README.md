# CSRF-and-XSS


# How to run the code:
  Navigate to the root directory and install all the necessary libraries. 
  To demonstrate XSS attack:-
      - Open two terminals. Enter the command python3 server.py host => For Victim side and python3 server.py attacker for Hacker side
      - From the hacker's wallet transfer the amount to Victim's account and enter malicious script in Reason textarea
      
  To demonstrate CSRF attack:-
      - Open terminal and enter the command python3 csrf_attack.py. Click on the button and $5000 will be transfered to attacker's wallet

Demostrated the working of CSRF and XSS attack by banking example.

CSRF :- Also known as Cross-site request forgery. CSRF attack occurs when a user's browser visits a trusted website while being directed to a malicious website. This might be executed through a link via email or chat
        Examples: Transfer money out of user’s account
                  Change in email address
                  Compromise user accounts


XSS :- Also known as Cross-site scripting. It uses the website as a means to attack user. Code injection attack allows injections of malicious code into the website. Used to steal user cookies, allowing for someone to use their website


CSRF Prevention
  - All the POST requests must contain a pseudo-random value (a token value)
  - Every time when user submit the form, the token value should be included in it
  - Adding additional authentication step before critical actions
XSS Prevention
  - Authentication and Authorization
  = Filter input on arrival
  - Encode data on output
  - Use web application firewall (WAF) to detect and block malicious user
  
  
  
