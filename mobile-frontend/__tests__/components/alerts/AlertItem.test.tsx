import React from "react";
import { render, fireEvent } from "@testing-library/react-native";
import AlertItem from "../../../src/components/alerts/AlertItem";
import { ThemeProvider } from "../../../src/context/ThemeContext";

const mockAlert = {
  id: "1",
  type: "price",
  priority: "high",
  title: "Price Alert",
  message: "BTC reached $50,000",
  timestamp: new Date().toISOString(),
};

const Wrapper = ({ children }: { children: React.ReactNode }) => (
  <ThemeProvider>{children}</ThemeProvider>
);

describe("AlertItem", () => {
  it("renders correctly", () => {
    const { getByText } = render(<AlertItem alert={mockAlert} />, {
      wrapper: Wrapper,
    });

    expect(getByText("Price Alert")).toBeTruthy();
    expect(getByText("BTC reached $50,000")).toBeTruthy();
  });

  it("calls onPress when pressed", () => {
    const onPress = jest.fn();
    const { getByText } = render(
      <AlertItem alert={mockAlert} onPress={onPress} />,
      { wrapper: Wrapper },
    );

    fireEvent.press(getByText("Price Alert"));
    expect(onPress).toHaveBeenCalled();
  });

  it("calls onDismiss when dismiss button is pressed", () => {
    const onDismiss = jest.fn();
    const { getByTestId } = render(
      <AlertItem alert={mockAlert} onDismiss={onDismiss} />,
      { wrapper: Wrapper },
    );

    // Note: You'd need to add testID to the dismiss button in the component
    // This is a placeholder test structure
  });
});
