# frozen_string_literal: true

class JobType < ApplicationRecord
  before_save :nullify_blanks

  belongs_to :user
  has_many :jobs
  has_many :event_receivers

  private

  def nullify_blanks
    update(environment_variables: "{}") if environment_variables&.empty?
    update(working_directory: nil) if working_directory&.empty?
  end
end
