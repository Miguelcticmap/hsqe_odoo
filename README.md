# HSEQ Management System — MAPEI Colombia (Odoo 19 Community)

Sistema integral de gestión **HSEQ (Health, Safety, Environment & Quality)** desarrollado exclusivamente para **Odoo 19 Community**, con la **Sede** como eje de segmentación operativa:

```
MAPEI Colombia → Sede → Área → Proceso → Actividad → Gestión HSEQ
```

## Módulos incluidos

| Módulo | Descripción |
|---|---|
| `hseq_core` | **Núcleo (instalar primero).** Sedes, áreas, procesos, actividades, mixin transversal, grupos de seguridad, seguridad por sede, menú principal HSEQ |
| `hseq_action_plan` | Planes de acción transversales (ACC-) con estados, avance, verificación y eficacia |
| `hseq_risk` | Matriz de riesgos (RSG-): peligros, evaluación 5×5, controles, riesgo inherente y residual |
| `hseq_incidents` | Incidentes/accidentes (INC-): reporte → investigación → análisis causal → plan de acción → cierre |
| `hseq_inspections` | Plantillas de inspección + ejecución (INS-) con generación automática de acciones por hallazgo |
| `hseq_epp` | Catálogo de EPP y entregas (EPP-) con aceptación del empleado |
| `hseq_nonconformity` | No conformidades (NC-) con flujo completo hasta verificación de eficacia |
| `hseq_audit` | Auditorías (AUD-) internas/externas con hallazgos y generación de NC |
| `hseq_quality` | Oportunidades de mejora (MEJ-), integra NC y auditorías |
| `hseq_sst` | Módulo paraguas SST (instala riesgos + incidentes + inspecciones + EPP + capacitaciones) |
| `hseq_environment` | Aspectos e impactos ambientales (ASP-) y registro de consumos (agua, energía…) |
| `hseq_waste` | Gestión de residuos (RES-) con clasificación, gestor y certificado de disposición |
| `hseq_documents` | Gestión documental: versionado, flujo Borrador → Revisión → Aprobación → Vigente → Obsoleto |
| `hseq_training` | Cursos y sesiones de capacitación (CAP-) con asistencia, evaluación y vencimientos |
| `hseq_contractors` | Habilitación de contratistas (CTR-): documentación, personal, sedes autorizadas |
| `hseq_compliance` | Requisitos legales (REQ-) con periodicidad, fecha límite y estado de cumplimiento |
| `hseq_indicators` | Indicadores configurables con metas y mediciones por sede/periodo |
| `hseq_dashboard` | Dashboard HSEQ MAPEI con KPIs filtrables por sede |

## Instalación

1. Copiar **todas** las carpetas `hseq_*` a la ruta de addons, por ejemplo:
   ```
   C:\odoo\odoo\odoo\my_modules\
   ```
2. Verificar que la ruta esté en `addons_path` del archivo `odoo.conf`:
   ```
   addons_path = C:\odoo\odoo\odoo\addons, C:\odoo\odoo\odoo\my_modules
   ```
3. Reiniciar el servicio de Odoo.
4. Activar el modo desarrollador → **Aplicaciones → Actualizar lista de aplicaciones**.
5. Instalar la app **HSEQ Core** (instala automáticamente sus dependencias `base`, `mail`, `web`).
6. Instalar los módulos deseados. Para toda la suite, instalar **hseq_sst**, **hseq_quality**, **hseq_environment**, **hseq_waste**, **hseq_documents**, **hseq_contractors**, **hseq_compliance**, **hseq_indicators** y **hseq_dashboard** (el resto se instala por dependencia).

## Seguridad

Grupos (Ajustes → Usuarios → pestaña de accesos, privilegio **HSEQ**):

- **HSEQ Usuario** → consulta, reporta incidentes, ejecuta inspecciones asignadas
- **HSEQ Responsable** → gestiona registros, acciones, inspecciones, capacitaciones
- **HSEQ Auditor** → ejecuta auditorías y registra hallazgos
- **HSEQ Supervisor** → revisa, aprueba y cierra; ve indicadores
- **HSEQ Administrador** → configuración completa

**Seguridad por sede:** en la ficha del usuario (pestaña *HSEQ*) se asignan las *Sedes HSEQ autorizadas*. Un usuario con sedes asignadas solo ve registros de esas sedes; sin sedes asignadas ve todas. Los administradores HSEQ siempre ven todas las sedes.

## Notas técnicas (Odoo 19)

- Vistas con etiqueta `<list>` (no `<tree>`) y `view_mode="list,form"`.
- Expresiones directas `invisible="state != 'draft'"` (sin `attrs`/`states`).
- Chatter con la etiqueta `<chatter/>`.
- Grupos con `res.groups.privilege` + `privilege_id` (nuevo modelo de privilegios de Odoo 19).
- Sin dependencias Enterprise ni de `sale`, `purchase`, `account`, `crm` o `helpdesk`. Solo `base`, `mail`, `web`.
- Trazabilidad con `mail.thread` + `mail.activity.mixin` en todos los registros críticos.
- Secuencias `ir.sequence` por documento y reglas de registro (`ir.rule`) por sede.
