document.getElementById("registerForm").addEventListener("submit", async function(e){
    e.preventDefault();

    const form = e.target;
    const data = {
        name: form.name.value.trim(),
        email: form.email.value.trim(),
        password: form.password.value.trim(),
        phone: form.phone.value.trim(),
         role: "customer"
    };


    try{
        const res = await fetch("http://localhost:5000/api/customers/register", {
            method: "POST",
            headers:{"Content-Type": "application/json"},
            body: JSON.stringify(data),
        });

        const result = await res.json();
        const messageBox = document.getElementById("message");
        if(res.ok){
            messageBox.textContent = "Register Successful!";
            messageBox.style.color = "green";
            form.reset();
        }else{
            messageBox.textContent = `${result.error || "Registration failed"}`;
            messageBox.style.color = "red";
        }
    }catch(err) {
        console.error("Request failed!", err);
    }


});