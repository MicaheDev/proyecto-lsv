import {
  HandPointingIcon,
  HouseIcon,
  TrophyIcon,
  UserCircleIcon,
} from "@phosphor-icons/react";

export default function BottomBar() {
  return (
    <div className="h-20 w-full flex border-t justify-between gap-2 items-center px-6">
      <button className="flex items-center justify-center p-2 border rounded-2xl bg-white">
        <HouseIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-blue-400"
          size={36}
        />
      </button>

      <button className="flex items-center justify-center p-2 rounded-2xl">
        <HandPointingIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-orange-300"
          size={36}
        />
      </button>

      <button className="flex items-center justify-center p-2 rounded-2xl">
        <TrophyIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-yellow-300"
          size={36}
        />
      </button>

      <button className="flex items-center justify-center p-2 rounded-2xl">
        <UserCircleIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-indigo-300"
          size={36}
        />
      </button>
    </div>
  );
}
