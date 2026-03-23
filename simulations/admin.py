from django.contrib import admin
from .models import SimulationLog


@admin.register(SimulationLog)
class SimulationLogAdmin(admin.ModelAdmin):
    list_display = ['simulation_type', 'user', 'simulated_latency_ms',
                    'simulated_tokens', 'simulated_cost_usd', 'created_at']
    list_filter = ['simulation_type']
    readonly_fields = ['parameters', 'result']
