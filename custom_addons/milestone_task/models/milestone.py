# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    milestone = fields.Integer("Milestone",
                               help="Creates task based on the value given in milestone")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    project_id = fields.Many2one(comodel_name='project.project')
    project_create = fields.Boolean()

    def button_create_project(self):
        """Function to create a project when clicking the Create Project button
        if there are 4 order lines and 2 order lines has milestone 2 and 2 has milestone 3
        then create a project with name as SO and tasks as Milestone 2 & milestone 3
        and subtasks as Milestone 2 - product name & milestone3 - Product name"""

        self.project_create = True
        milestone_dict = {}
        project = self.env['project.project'].create({
            'name': self.name,
            'partner_id': self.partner_id.id,
        })

        self.project_id = project

        for record in self.order_line:
            if record.milestone not in milestone_dict:
                task = self.env['project.task'].create({
                    'name': f'Milestone{record.milestone}',
                    'project_id': project.id
                })

                self.env['project.task'].create({
                    'name': f'Milestone{record.milestone} - {record.product_template_id.name}',
                    'parent_id': task.id
                })
                milestone_dict[record.milestone] = task.id
            else:
                self.env['project.task'].create({
                    'name': f'Milestone{record.milestone} - {record.product_template_id.name}',
                    'parent_id': milestone_dict[record.milestone]
                })

    def action_view_project_ids(self):
        """Function to show task kanban view in the smart-tab of project in sales"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Project',
            'view_mode': 'kanban,form',
            'res_model': 'project.task',
            'domain': [('display_project_id', '=', self.project_id.id)],
            'views': [(self.env.ref('project.view_task_kanban').id, 'kanban'), (False, 'form')],
            'context': {'active_id': self.project_id.id},
            'target': 'current',
        }

    def button_update_project(self):
        """Function to update the already created task if any changes are made"""

        if self.project_id:
            milestones = self.milestone_listing()
            print(milestones, "qqq")
            task_list = []
            for milestone, product in milestones.items():
                task_name = f'Milestone{milestone}'
                task_list.append(task_name)

                main_task = self.project_id.task_ids.filtered(lambda rec: rec.name == task_name)

                if not main_task:
                    main_task = self.env['project.task'].create({
                        'name': task_name,
                        'project_id': self.project_id.id
                    })

                for record in product:
                    subtask_name = f'Milestone{milestone} - {record.product_template_id.name}'
                    task_list.append(subtask_name)
                    task = self.project_id.task_ids.filtered(lambda rec: rec.name == subtask_name)

                    if not task:
                        self.env['project.task'].create({
                            'name': subtask_name,
                            'parent_id': main_task.id
                        })

            for child in self.project_id.task_ids.filtered(lambda rec: rec.name not in task_list):
                main_task.child_ids = [fields.Command.delete(child.id)]

    def milestone_listing(self):
        milestones = {}
        for line in self.order_line:
            if line.milestone not in milestones:
                milestones[line.milestone] = []
            milestones[line.milestone].append(line)
        return milestones
