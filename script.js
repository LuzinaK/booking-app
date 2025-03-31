async function registreties() {
    const lietotajvards = document.getElementById("register-username").value;
    const parole = document.getElementById("register-password").value;
    const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: lietotajvards, password: parole })
    });
    alert((await response.json()).message);
}

async function pieslegties() {
    const lietotajvards = document.getElementById("login-username").value;
    const parole = document.getElementById("login-password").value;
    const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: lietotajvards, password: parole })
    });
    const data = await response.json();
    if (response.ok) {
        sessionStorage.setItem("loma", data.role);
        document.getElementById("auth").style.display = "none";
        document.getElementById("content").style.display = "block";
        ieladetTelpas();
        ieladetRezervacijas();
    } else {
        alert(data.message);
    }
}

async function atslegties() {
    await fetch("/logout", { method: "POST" });
    sessionStorage.removeItem("loma");
    document.getElementById("auth").style.display = "block";
    document.getElementById("content").style.display = "none";
}

async function ieladetTelpas() {
    const response = await fetch("/facilities");
    const telpas = await response.json();
    const saraksts = document.getElementById("facility-list");
    const izvele = document.getElementById("facility-select");
    saraksts.innerHTML = "";
    izvele.innerHTML = "";
    telpas.forEach(telpa => {
        const ieraksts = document.createElement("li");
        ieraksts.textContent = `${telpa.name} - ${telpa.capacity} cilvēki`;
        saraksts.appendChild(ieraksts);

        const opcija = document.createElement("option");
        opcija.value = telpa.id;
        opcija.textContent = telpa.name;
        izvele.appendChild(opcija);
    });
}

async function rezervetTelpu() {
    const telpas_id = document.getElementById("facility-select").value;
    const datums = document.getElementById("booking-date").value;
    const laiks = document.getElementById("booking-time").value;
    const response = await fetch("/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ facility_id: telpas_id, date: datums, time: laiks })
    });
    alert((await response.json()).message);
    ieladetRezervacijas();
}

async function ieladetRezervacijas() {
    const response = await fetch("/bookings");
    const rezervacijas = await response.json();
    const saraksts = document.getElementById("booking-list");
    saraksts.innerHTML = "";
    rezervacijas.forEach(rezervacija => {
        const ieraksts = document.createElement("li");
        ieraksts.textContent = `Telpas ID: ${rezervacija.facility_id}, Datums: ${rezervacija.date}, Laiks: ${rezervacija.time}`;
        saraksts.appendChild(ieraksts);
    });
}