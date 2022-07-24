const USERNAME = "admin-dicegang_pp_user";
const PASSWORD = "53d9d3e771374c39ca3b321ddfecddc1";

export default {
  id: 'payment-pal',
  name: 'payment-pal',
  timeout: 18000,
  handler: async (url, ctx) => {
    const page = await ctx.newPage();
    await page.goto("https://payment-pal.mc.ax", {
      waitUntil: "networkidle2"
    });

    await page.evaluate((username, password) => {
      document.querySelector("input[name=username]").value = username;
      document.querySelector("input[name=password]").value = password;
      document.querySelector("#login_btn").click();
    }, USERNAME, PASSWORD);
    page.once('dialog', async dialog => {
      await dialog.dismiss();
    });
    await page.waitForNavigation();

    // random wait just in case lmao
    await page.waitForTimeout(1000);

    await page.evaluate(() => {
      document.querySelector("#logout_btn").click();
    });

    await page.waitForTimeout(2000);

    await page.goto(url);
    await page.waitForTimeout(10000);
  },
}
