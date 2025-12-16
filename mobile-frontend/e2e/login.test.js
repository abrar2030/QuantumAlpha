describe("Login Flow", () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it("should show login screen", async () => {
    await expect(element(by.text("Login"))).toBeVisible();
  });

  it("should login with valid credentials", async () => {
    await element(by.id("email-input")).typeText("test@quantumalpha.com");
    await element(by.id("password-input")).typeText("password123");
    await element(by.id("login-button")).tap();

    // Should navigate to dashboard
    await waitFor(element(by.id("dashboard")))
      .toBeVisible()
      .withTimeout(5000);
  });

  it("should show error with invalid credentials", async () => {
    await element(by.id("email-input")).typeText("wrong@email.com");
    await element(by.id("password-input")).typeText("wrongpass");
    await element(by.id("login-button")).tap();

    await expect(element(by.text("Invalid credentials"))).toBeVisible();
  });
});
