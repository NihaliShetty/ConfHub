function getTopConf(){

  if (localStorage.getItem("email")) {
    document.getElementById("logOutBtn").innerHTML = "Log Out";
    var confNearMeBtn = document.getElementById("confNearMeBtn");
    var profileBtn = document.getElementById("profileBtn");
    confNearMeBtn.innerHTML = "Confs Near Me";
    confNearMeBtn.href = "/confs_near_me.html";
    profileBtn.innerHTML = "Profile";
    profileBtn.href = "/profile_page.html";
  }

  axios.post(SERVER_URL + "conferences-by-impact", {
    appToken: appToken
  }).then(response => {
    if (!response.data.success) {
      alert("Failed to obtain list of conferences from server. " + response.data.reason);
      return;
    }
    console.log(response.data.conferences);
    var container = document.getElementById("container1");
    container.innerHTML = "";
    var x = 0;
    for (var conf of response.data.conferences) {
      console.log(conf);
      var doc = document.createElement("div");
      doc.className = "button button4";
      // console.log(conf.id)
      var confid = document.createElement("div");
      confid.innerHTML = conf.id
      confid.style.display = "none";
      doc.appendChild(confid);

      var link = document.createElement("a");
      link.href = conf.link;
      link.textContent = conf.name;
      link.className = "linkconf"
      doc.appendChild(link);
      var date = document.createElement("div");
      date.textContent = conf.date;
      date.className = "date dateconf";
      var location = document.createElement("div");
      location.textContent = conf.location;
      location.className = "location locationconf";
      
      var container3 = document.createElement("div");
      // var organizer = document.createElement("div");
      // organizer.className = "organizer";
      // organizer.textContent = "Organized by " + conf.organizer;
      var category = document.createElement("div");
      category.className = "category categoryconf";
      category.textContent = "Impact Factor: " + conf.h_index;
      // container3.appendChild(organizer)
      container3.appendChild(category)
      doc.appendChild(date);
      doc.appendChild(location);
      doc.appendChild(container3)

      var hiddendiv = document.createElement("div");
      hiddendiv.innerHTML = conf;
      hiddendiv.style.display="none";
      doc.appendChild(hiddendiv);

      container.appendChild(doc);
      
      if(x==0){
        //somthing
        var cardcard = document.getElementById("cardcard");
        cardcard.innerHTML="";
        var hiddiv1 = document.createElement("div");
        hiddiv1.innerHTML = conf.name;
        hiddiv1.style.display = "none";

        var hiddiv2 = document.createElement("div");
        hiddiv2.innerHTML = conf.location;
        hiddiv2.style.display = "none";

        var confInfo = document.createElement("div");
        confInfo.style.padding = "15px";
        var link1 = document.createElement("a");
        link1.href = conf.website;
        link1.textContent = "Link to Website";
        link1.style.fontSize = "large";
        
        // var div2 = document.createElement("div");
        // div2.innerHTML = "Organizer Email : "+conf.email;
        var div6 = document.createElement("div");
        div6.innerHTML = "Organized By : "+conf.organizer;
        var div3 = document.createElement("div");
        div3.innerHTML = "Deadline Date : "+conf.deadline;
        var div4 = document.createElement("div");
        div4.innerHTML = "Country : "+conf.country;
        // var div5 = document.createElement("div");
        // div5.style.paddingTop = "3%";
        // div5.innerHTML = conf.h_index;
        
        confInfo.appendChild(hiddiv1);
        confInfo.appendChild(hiddiv2);

        confInfo.appendChild(link1);
        // confInfo.appendChild(div2);
        confInfo.appendChild(div3);
        confInfo.appendChild(div4)
        confInfo.appendChild(div6);
        // confInfo.appendChild(div5);

        // var inputtag = document.createElement("input");
        // inputtag.type = "text";
        // inputtag.className = "form-control inputtag";
        // inputtag.placeholder = "Add Email...";
        // inputtag.style.width = "70%";
        var alertButton = document.createElement("div");
        alertButton.className = "alertButton";
        alertButton.innerHTML="Alert for conf";
        cardcard.appendChild(confInfo);
        // cardcard.appendChild(inputtag);
        cardcard.appendChild(alertButton);
        alertButton.addEventListener('click', function() {
          var deadline = this.parentElement.childNodes[0].childNodes[3].innerHTML.split(":")[1].trim() ;
          var email = this.parentElement.childNodes[1].value;
          var name = this.parentElement.childNodes[0].childNodes[0].innerHTML.trim();
          var location = this.parentElement.childNodes[0].childNodes[1].innerHTML;
          console.log(deadline);
          console.log(email);

          console.log(name);
          console.log(location);
          var email = localStorage.getItem("email");
          var token = localStorage.getItem("userToken");
          axios.post(SERVER_URL + "mail", {
            userToken:token,
            email: email,
            deadline:deadline,
            confname:name,
            location:location
          }).then(response => {
            if (!response.data.already_subscribed) {
              // alert("Failed to send alert" + response.data.reason);
              alert("Subscribed");
              return;
            }
            alert("Already subscribed");
          }); // end of mail request.
         
          
        }); // end of event listener alert button
        x = x + 1;
      }
      doc.addEventListener("click",function() {
        var cardcard = document.getElementById("cardcard");
        cardcard.innerHTML = "";                
        var confid = this.childNodes[0].innerHTML;
        console.log(confid);
        axios.post(SERVER_URL + "conferences-by-impact", {
          appToken: appToken
        }).then(response => {
          if (!response.data.success) {
            alert("Failed to obtain list of conferences from server. " + response.data.reason);
            return;
          }
          for (var conf of response.data.conferences) {
            if(conf.id == confid) {
              console.log(conf)
              // var organizedBy = document.createElement("div");
              // organizedBy.innerHTML="Organized by : "+ conf.organizer;
              var cardcard = document.getElementById("cardcard");
              // cardcard.innerHTML=;
              var hiddiv1 = document.createElement("div");
              hiddiv1.innerHTML = conf.name;
              hiddiv1.style.display = "none";

              var hiddiv2 = document.createElement("div");
              hiddiv2.innerHTML = conf.location;
              hiddiv2.style.display = "none";

              var confInfo = document.createElement("div");
              confInfo.style.padding = "15px";
              // confInfo.style.width = "200px";
              var link1 = document.createElement("a");
              link1.href = conf.website;
              link1.textContent = "Link to Website";
              link1.style.fontSize = "large";
              
              // var div2 = document.createElement("div");
              // div2.innerHTML = "Organizer Email : "+conf.email;
              var div6 = document.createElement("div");
              div6.innerHTML = "Organized By : "+conf.organizer;
              var div3 = document.createElement("div");
              div3.innerHTML = "Deadline Date : "+conf.deadline;
              var div4 = document.createElement("div");
              div4.innerHTML = "Country : "+conf.country;
              // var div5 = document.createElement("div");
              // div5.style.paddingTop = "3%";
              // div5.innerHTML = conf.description;
              
              confInfo.appendChild(hiddiv1);
              confInfo.appendChild(hiddiv2);

              confInfo.appendChild(link1);
              // confInfo.appendChild(div2);
              confInfo.appendChild(div3);
              confInfo.appendChild(div4)
              confInfo.appendChild(div6);
              // confInfo.appendChild(div5);

              // var inputtag = document.createElement("input");
              // inputtag.type = "text";
              // inputtag.className = "form-control inputtag";
              // inputtag.placeholder = "Add Email...";
              // inputtag.style.width = "70%";
              var alertButton = document.createElement("div");
              alertButton.className = "alertButton";
              alertButton.innerHTML="Alert for conf";
              cardcard.appendChild(confInfo);
              // cardcard.appendChild(inputtag);
              cardcard.appendChild(alertButton);
              alertButton.addEventListener('click', function() {
                var deadline = this.parentElement.childNodes[0].childNodes[3].innerHTML.split(":")[1].trim() ;
                var email = this.parentElement.childNodes[1].value;
                var name = this.parentElement.childNodes[0].childNodes[0].innerHTML.trim();
                var location = this.parentElement.childNodes[0].childNodes[1].innerHTML;
                console.log(deadline);
                console.log(email);
      
                console.log(name);
                console.log(location);
                var email = localStorage.getItem("email");
                var token = localStorage.getItem("userToken");
                axios.post(SERVER_URL + "mail", {
                  // appToken : appToken,
                  userToken:token,
                  email: email,
                  deadline:deadline,
                  confname:name,
                  location:location
                }).then(response => {
                  if (!response.data.already_subscribed) {
                    // alert("Failed to send alert" + response.data.reason);
                    alert("Subscribed");
                    return;
                  }
                  alert("Already subscribed");
                }); // end of mail request.
               
               
              }); // end of event listener alert button
              break;
            }
          }
        }); // confid request
        
        
    });//end of doc event listener
    } // end of for loop for list of conferences.
  });

             
}