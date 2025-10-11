// "use client";

// import { ChatStream } from "@/components/chat/ChatStream";

// export default function Home() {
//   return (
//     <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900 text-white">
//       <div className="w-full max-w-3xl p-4">
//         <h1 className="text-4xl font-bold text-center mb-2">IntelliAgent</h1>
//         <p className="text-center text-gray-400 mb-8">
//           Phase 2: Agentic Orchestration with Real-time Streaming
//         </p>
//         <ChatStream />
//       </div>
//     </main>
//   );
// }


"use client";

import { ChatStream } from "@/components/chat/ChatStream";

export default function Home() {
  return (
    <div className="h-screen">
      <ChatStream />
    </div>
  );
}
