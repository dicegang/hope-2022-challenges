async function checkSolve(input) {
  const flagPt1 =
    String.fromCharCode(148 - eval.toString().length) +
    String.fromCharCode((window.frames.length !== -1) * 72) +
    String.fromCharCode((navigator.onLine + screen.orientation.angle) * 111) +
    String.fromCharCode(
      (performance.mark({}).name === "[object Object]") * 101
    );

  const msgBuffer = new TextEncoder().encode(flagPt1);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hash = hashArray
    .map(function (b) {
      return b.toString(16).padStart(2, "0");
    })
    .join("");
  const flagPt2 = hash.slice(0, 16);

  if (input === "hope{" + flagPt1 + "_" + flagPt2 + "_sold!}") {
    console.log("you got it!");
  } else {
    console.log("wrong flag :(");
  }
}
