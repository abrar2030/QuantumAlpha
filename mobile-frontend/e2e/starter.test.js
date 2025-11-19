// This file would contain basic end-to-end tests for the mobile application using a framework like Detox.
// Example: login flow, viewing portfolio, placing orders.

describe("Login Flow", () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it("should have welcome screen", async () => {
    await expect(element(by.id("welcome"))).toBeVisible();
  });

  it("should be able to login with valid credentials", async () => {
    await element(by.id("usernameInput")).typeText("testuser");
    await element(by.id("passwordInput")).typeText("password");
    await element(by.id("loginButton")).tap();
    await expect(element(by.id("dashboardScreen"))).toBeVisible();
  });
});
