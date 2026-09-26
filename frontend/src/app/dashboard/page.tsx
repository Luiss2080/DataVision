export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight mb-8">Resumen de Datos</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {[
          { title: "Usuarios Activos", value: "1,248", change: "+12%" },
          { title: "Ingresos Brutos", value: "$42,390", change: "+8.4%" },
          { title: "Peticiones API", value: "849k", change: "-2.1%" }
        ].map((stat, i) => (
          <div key={i} className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 p-6 rounded-2xl shadow-sm">
            <h3 className="text-zinc-500 dark:text-zinc-400 text-sm font-medium mb-2">{stat.title}</h3>
            <div className="flex items-end justify-between">
              <span className="text-3xl font-bold">{stat.value}</span>
              <span className={`text-sm font-medium ${stat.change.startsWith('+') ? 'text-green-500' : 'text-red-500'}`}>
                {stat.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-zinc-800 h-96 rounded-2xl flex items-center justify-center shadow-sm">
        <p className="text-zinc-500">Aquí irá el gráfico interactivo (Recharts/Chart.js)</p>
      </div>
    </div>
  );
}
