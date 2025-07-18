
document.getElementById("activationForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const form = e.target;
    const data = {
        name: form.name.value.trim(),
        phone: form.phone.value.trim(),
        plate_letters: form.plate_letters.value.trim(),
        plate_numbers: form.plate_numbers.value.trim(),
        code: form.code.value.trim()
    };

    const response = await fetch("/activate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    const alertBox = document.getElementById("alert");
    alertBox.style.display = "block";
    alertBox.textContent = result.message;
    alertBox.className = "alert " + (result.success ? "success" : "error");
});
