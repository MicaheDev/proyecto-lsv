import { Outlet } from "react-router"

type Props = {}

export default function Layout({}: Props) {
  return (
    <div className="w-full h-full bg-yellow-50 text-neutral-700">
        <Outlet/>
    </div>
  )
}