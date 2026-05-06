import { useState } from "react";
import Scaffold from "../components/Scaffold";
import TopBar from "../components/TopBar";
import BottomBar from "../components/BottomBar";
import Onboarding from "../components/Onboarding";

export default function Home() {
  const [isFirstTime, setIsFirstTime] = useState(true);

  console.log(setIsFirstTime);

  if (isFirstTime) return <Onboarding />;

  return <Scaffold TopBar={<TopBar />} BottomBar={<BottomBar />} />;
}
