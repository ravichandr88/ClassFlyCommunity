let d = document.getElementById("days");
let h = document.getElementById("hour");
let m = document.getElementById("min");
let s = document.getElementById("sec");

let count = new Date("1 jan ,2022 04:00:00").getTime();

let x = setInterval(function () {
  let now = new Date().getTime();
  let D = count - now;

  let days = Math.round(D / (1000 * 60 * 60 * 24));
  let hour = Math.round((D % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  let min = Math.round((D % (1000 * 60 * 60)) / (1000 * 60));
  let sec = Math.round((D % (1000 * 60)) / 1000);

  d.innerHTML = days;
  h.innerHTML = hour;
  m.innerHTML = min;
  s.innerHTML = sec;

  if (days < 10) {
    d.innerHTML = "0" + days;
  }
  if (hour < 10) {
    h.innerHTML = "0" + hour;
  }
  if (min < 10) {
    m.innerHTML = "0" + min;
  }
  if (sec < 10) {
    s.innerHTML = "0" + sec;
  }
  if (D < 0) {
    clearInterval();

    d.innerHTML = "---";
    h.innerHTML = "---";
    m.innerHTML = "---";
    s.innerHTML = "---";

    document.getElementById("expiredtext1").innerHTML = "event expired";
    document.getElementById("expiredtext2").innerHTML = "try again";
    document.getElementById(
      "expiredtext3"
    ).innerHTML = `“Creativity is just connecting things.”<br>
    ― Steve Jobs`;
  }
}, 1000);